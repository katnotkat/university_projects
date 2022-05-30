from collections import defaultdict

import numpy as np
import seaborn as sns
from sklearn.metrics import roc_auc_score
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt


sns.set(style='darkgrid')


def score(clf, x, y):
    return roc_auc_score(y == 1, clf.predict_proba(x)[:, 1])


class Boosting:

    def __init__(
            self,
            base_model_params: dict = None,
            n_estimators: int = 10,
            learning_rate: float = 0.1,
            subsample: float = 0.3,
            early_stopping_rounds: int = None,
            plot: bool = False,
    ):
        self.base_model_class = DecisionTreeRegressor
        self.base_model_params: dict = {} if base_model_params is None else base_model_params

        self.n_estimators: int = n_estimators

        self.models: list = []
        self.gammas: list = []

        self.learning_rate: float = learning_rate
        self.subsample: float = subsample

        self.early_stopping_rounds: int = early_stopping_rounds
        if early_stopping_rounds is not None:
            self.validation_loss = np.full(self.early_stopping_rounds, np.inf)

        self.plot: bool = plot

        self.history = defaultdict(list)

        self.sigmoid = lambda x: 1 / (1 + np.exp(-x))
        self.loss_fn = lambda y, z: -np.log(self.sigmoid(y * z)).mean()
        self.loss_derivative = lambda y, z: -y * self.sigmoid(-y * z)
        self.loss_derivative2 = lambda y, z: y ** 2 * self.sigmoid(-y * z) * (1 - self.sigmoid(-y * z))

    def fit_new_base_model(self, x, y, predictions):
        # bootstrap
        l = x.shape[0]
        ind = np.random.choice(l, int(l * self.subsample))
        # base model fitting
        model = self.base_model_class(**self.base_model_params)
        s = self.loss_derivative(y[ind], predictions[ind]) / self.loss_derivative2(y[ind], predictions[ind])
        model.fit(x[ind], -s)
        preds = model.predict(x)
        
        # finding gamma
        gamma = self.find_optimal_gamma(y, predictions, preds)
        
        self.gammas.append(gamma)
        self.models.append(model)
        return gamma * self.learning_rate * preds

    def fit(self, x_train, y_train, x_valid, y_valid):
        """
        :param x_train: features array (train set)
        :param y_train: targets array (train set)
        :param x_valid: features array (validation set)
        :param y_valid: targets array (validation set)
        """
        self.history['train_loss'] = []
        self.history['val_loss'] = []
        self.history['score'] = []
        train_predictions = np.zeros(y_train.shape[0])
        valid_predictions = np.zeros(y_valid.shape[0])

        for _ in range(self.n_estimators):
            # updating predictions
            train_predictions += self.fit_new_base_model(x_train, y_train, train_predictions)
            valid_predictions += self.gammas[-1] * self.learning_rate * self.models[-1].predict(x_valid)
            
            self.history['train_loss'].append(self.loss_fn(y_train, train_predictions))
            self.history['val_loss'].append(self.loss_fn(y_valid, valid_predictions))
            self.history['score'].append(self.score(x_valid, y_valid))
            
            if self.early_stopping_rounds is not None:
                self.validation_loss.append(history['val_loss'][-1])
                self.validation_loss = self.validation_loss[-self.early_stopping_rounds:]
                if (self.validation_loss == np.sort(self.validation_loss)).all():
                    break

        if self.plot:
            plt.plot(range(1, self.n_estimators + 1), self.history['train_loss'], c='b', label='Train loss')
            plt.plot(range(1, self.n_estimators + 1), self.history['val_loss'], c='r', label='Validation loss')
            plt.xlabel('n_estimators')
            plt.ylabel('loss')
            plt.legend()
            plt.show()
            
            plt.plot(range(1, self.n_estimators + 1), self.history['score'])
            plt.xlabel('n_estimators')
            plt.ylabel('auc-roc score')
            plt.show()

    def predict_proba(self, x):
        preds = np.zeros((x.shape[0], 2))
        for gamma, model in zip(self.gammas, self.models):
            preds[:, 1] += model.predict(x) * gamma * self.learning_rate
        
        preds[:, 1] = self.sigmoid(preds[:, 1])
        preds[:, 0] = 1 - preds[:, 1]
        return preds

    def find_optimal_gamma(self, y, old_predictions, new_predictions) -> float:
        gammas = np.linspace(start=0, stop=1, num=100)
        losses = [self.loss_fn(y, old_predictions + gamma * new_predictions) for gamma in gammas]

        return gammas[np.argmin(losses)]

    def score(self, x, y):
        return score(self, x, y)

    @property
    def feature_importances_(self):
        pass
