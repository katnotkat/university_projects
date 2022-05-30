import numpy as np
from collections import Counter
from sklearn.base import BaseEstimator, ClassifierMixin


def find_best_split(feature_vector, target_vector):
    """
    Под критерием Джини здесь подразумевается следующая функция:
    $$Q(R) = -\frac {|R_l|}{|R|}H(R_l) -\frac {|R_r|}{|R|}H(R_r)$$,
    $R$ — множество объектов, $R_l$ и $R_r$ — объекты, попавшие в левое и правое поддерево,
    $H(R) = 1-p_1^2-p_0^2$, $p_1$, $p_0$ — доля объектов класса 1 и 0 соответственно.

    Указания:
    * Пороги, приводящие к попаданию в одно из поддеревьев пустого множества объектов, не рассматриваются.
    * В качестве порогов, нужно брать среднее двух сосдених (при сортировке) значений признака
    * Поведение функции в случае константного признака может быть любым.
    * При одинаковых приростах Джини нужно выбирать минимальный сплит.
    * За наличие в функции циклов балл будет снижен. Векторизуйте! :)

    :param feature_vector: вещественнозначный вектор значений признака
    :param target_vector: вектор классов объектов,  len(feature_vector) == len(target_vector)

    :return thresholds: отсортированный по возрастанию вектор со всеми возможными порогами, по которым объекты можно
     разделить на две различные подвыборки, или поддерева
    :return ginis: вектор со значениями критерия Джини для каждого из порогов в thresholds len(ginis) == len(thresholds)
    :return threshold_best: оптимальный порог (число)
    :return gini_best: оптимальное значение критерия Джини (число)
    """
    # indexes of sorted feature vector
    sorted_ind = np.argsort(feature_vector)
    # sorting feature + target by indexes above
    feature = feature_vector[sorted_ind]
    target = target_vector[sorted_ind]

    target_cumsum = np.cumsum(target) # sum of ones before
    # getting unique values, indexes of first occurence, counts
    unique, index, counts = np.unique(feature, return_index=True, return_counts=True)
    
    # to get how many ones are to the left from the threshold
    # we get indexes of the last occurence of each element
    # then use target_cumsum elements with corresponding indexes
    left_ones = target_cumsum[np.append((index[1:] - 1), [-1])][:-1]
    # ones on the right side of each threshold = ones overall - ones on the left side
    right_ones = (np.sum(target) - left_ones)
    els_left = np.cumsum(counts)[:-1] # how many elements are on the left side of the threshold
    size = target.size

    h_left = 1 - ((els_left - left_ones)/els_left)**2 - (left_ones/els_left)**2
    h_right = 1 - ((size - els_left - right_ones)/(size - els_left))**2 - (right_ones/(size - els_left))**2
    h_left *= els_left / size
    h_right *= (size - els_left) / size

    thresholds = (unique[:-1] + unique[1:]) / 2
    q_r = (- h_left - h_right)
    return tuple([thresholds, q_r, thresholds[np.argmax(q_r)], np.max(q_r)])


class DecisionTree:
    def __init__(self, feature_types, max_depth=None, min_samples_split=None, min_samples_leaf=None):
        if np.any(list(map(lambda x: x != "real" and x != "categorical", feature_types))):
            raise ValueError("There is unknown feature type")

        self._tree = {}
        self._feature_types = feature_types
        self._max_depth = max_depth
        self._min_samples_split = min_samples_split
        self._min_samples_leaf = min_samples_leaf

    def _fit_node(self, sub_X, sub_y, node):
        if np.all(sub_y == sub_y[0]):
            node["type"] = "terminal"
            node["class"] = sub_y[0]
            return

        feature_best, threshold_best, gini_best, split = None, None, None, None
        for feature in range(0, sub_X.shape[1]):
            feature_type = self._feature_types[feature]
            categories_map = {}

            if feature_type == "real":
                feature_vector = sub_X[:, feature]
            elif feature_type == "categorical":
                # сортировка признака по доле единиц в ответах
                counts = Counter(sub_X[:, feature]) # какие категории в Х, как часто встречается каждая
                clicks = Counter(sub_X[sub_y == 1, feature]) # у каких категорий единичный ответ
                ratio = {}
                for key, current_count in counts.items():
                    if key in clicks: # если категория дает ответ 1
                        current_click = clicks[key] # сколько раз?
                    else: # если только 0
                        current_click = 0
                    ratio[key] = current_click / current_count # доля единичных ответов для каждой категории
                sorted_categories = list(map(lambda x: x[0], sorted(ratio.items(), key=lambda x: x[1])))
                categories_map = dict(zip(sorted_categories, list(range(len(sorted_categories)))))

                feature_vector = np.array(list(map(lambda x: categories_map[x], sub_X[:, feature])))
            else:
                raise ValueError

            # если все значения признака одинаковые, то нет смысла искать порог
            if len(set(feature_vector)) == 1:
                continue

            _, _, threshold, gini = find_best_split(feature_vector, sub_y)
            if gini_best is None or gini > gini_best:
                feature_best = feature
                gini_best = gini
                split = feature_vector < threshold

                if feature_type == "real":
                    threshold_best = threshold
                elif feature_type == "categorical":
                    threshold_best = list(map(lambda x: x[0],
                                              filter(lambda x: x[1] < threshold, categories_map.items())))
                else:
                    raise ValueError
        
        if feature_best is None:
            node["type"] = "terminal"
            node["class"] = Counter(sub_y).most_common(1)[0][0]
            return

        node["type"] = "nonterminal"

        node["feature_split"] = feature_best
        if self._feature_types[feature_best] == "real":
            node["threshold"] = threshold_best
        elif self._feature_types[feature_best] == "categorical":
            node["categories_split"] = threshold_best
        else:
            raise ValueError
        node["left_child"], node["right_child"] = {}, {}
        self._fit_node(sub_X[split], sub_y[split], node["left_child"])
        self._fit_node(sub_X[np.logical_not(split)], sub_y[np.logical_not(split)], node["right_child"])

    def _predict_node(self, x, node):
        if node["type"] == "terminal":
            return node['class']
        
        feature = node["feature_split"]
        if self._feature_types[feature] == "real":
            if x[feature] <= node["threshold"]:
                return self._predict_node(x, node["left_child"])
            else:
                return self._predict_node(x, node["right_child"])
        elif self._feature_types[feature] == "categorical":
            if x[feature] in node["categories_split"]:
                return self._predict_node(x, node["left_child"])
            else:
                return self._predict_node(x, node["right_child"])
        else:
            raise ValueError

    def fit(self, X, y):
        self._fit_node(X, y, self._tree)

    def predict(self, X):
        predicted = []
        for x in X:
            predicted.append(self._predict_node(x, self._tree))
        return np.array(predicted)
    
    def get_params(self, deep = False):
        return {'feature_types': self._feature_types,
                'max_depth': self._max_depth,
                'min_samples_split': self._min_samples_split,
                'min_samples_leaf': self._min_samples_leaf}