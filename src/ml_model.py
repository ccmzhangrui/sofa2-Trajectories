import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score


def train_models(X_train, y_train):
    models = []
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    lgbm_model = LGBMClassifier(n_estimators=100, random_state=42)
    xgb_model = xgb.XGBClassifier(n_estimators=100, random_state=42,  use_label_encoder=False, eval_metric='logloss')
    for model in [lgbm_model, rf_model, xgb_model]:
        model.fit(X_train, y_train)
        models.append(model)
    return models


def soft_vote_predict(models, X):
    preds = [model.predict_proba(X)[:, 1] for model in models]
    return np.mean(preds, axis=0)


def evaluate_models(models, X_val, y_val):
    pred_prob = soft_vote_predict(models, X_val)
    auc = roc_auc_score(y_val, pred_prob)
    return auc
