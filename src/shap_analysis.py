import shap
import matplotlib.pyplot as plt


def shap_summary(model, X_val):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_val)
    shap.summary_plot(shap_values, X_val)


def shap_force_plot(model, X_val, index=0):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_val)
    shap.force_plot(explainer.expected_value, shap_values[index, :], X_val.iloc[index, :])
