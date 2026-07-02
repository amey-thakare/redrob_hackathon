import lightgbm as lgb
import numpy as np


class LearningToRank:

    def __init__(self):

        self.model = lgb.LGBMRanker(
            objective="lambdarank",
            metric="ndcg",
            n_estimators=200,
            learning_rate=0.05,
            num_leaves=31,
        )

    def fit(self, X, y, group):

        self.model.fit(
            X,
            y,
            group=group,
        )

    def predict(self, X):

        return self.model.predict(X)