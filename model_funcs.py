from pycaret.classification import *
from supportFunc import *
import shutil

numerical_tags = ["total_change", "total_add", "total_del", "total_fchange"]

categorical_tags = []

special_tags = ["fchange"]

def createNewModel(diff_path,test_path,model_save=f"current_model"):
    """Creates new model to be saved."""
    # Create table for modeling
    dataset = createPandasFrame(numerical_tags,categorical_tags,special_tags,diff_path,test_path)

    target_data = dataset.sample(frac=0.95, random_state=786)
    data_unseen = dataset.drop(target_data.index)
    target_data.reset_index(inplace=True, drop=True)
    data_unseen.reset_index(inplace=True, drop=True)
    print("Data for Modeling: " + str(target_data.shape))
    print("Unseen Data For Predictions: " + str(data_unseen.shape))

    # Setup preprocessing
    s = setup(
        target_data,
        target="result",
        numeric_features=numerical_tags,
        categorical_features=categorical_tags,
        silent=True,
        remove_perfect_collinearity=False
    )

    # Create Logitic regression model

    # best = compare_models()
    model = create_model("lr")

    # ****************************
    # Tune and then save the model:
    # ****************************

    print("Tuning the new model...")
    # lr = ensemble_model(best, method='Boosting', choose_better=True)
    model = tune_model(model)
    print("Sucessfully tuned model.")
    plot_model(model, save=True)

    save_model(model, model_save)
    shutil.copy(f"./{model_save}.pkl",f"./models/{model_save}.pkl")

def forcastPredictions(target_diff,model):
    """Uses existing model to make predictions."""
    pass