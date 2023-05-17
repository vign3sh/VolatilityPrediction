from django.conf import settings
import os
from glob import glob
import yfinance as yf
import joblib
import pandas as pd
from arch import arch_model

class GarchModel:
    """Class for training GARCH model and generating predictions.

    Atttributes
    -----------
    ticker : str
        Ticker symbol of the equity whose volatility will be predicted.
    model_directory : str
        Path for directory where trained models will be stored.

    Methods
    -------
    wrangle_data
        Generate equity returns from data in database.
    fit
        Fit model to training data.
    predict
        Generate volatilty forecast from trained model.
    dump
        Save trained model to file.
    load
        Load trained model from file.
    """

    def __init__(self, ticker):
    
        self.ticker = ticker
        self.model_directory = settings.MODEL_DIR

    def wrangle_data(self):

        """Extract data from database (or get from AlphaVantage), transform it
        for training model, and attach it to `self.data`.

        Parameters
        ----------
        n_observations : int
            Number of observations to retrieve from database

        Returns
        -------
        None
        """
        

        # Get table from database
        df = yf.download(self.ticker,period = "10y")
        
        # Sort DataFrame ascending by date
        df.sort_index(ascending=True, inplace=True)

        # Create "return" column
        df['return'] = df['Close'].pct_change()*100

        # Return returns
        self.data = df['return'].dropna()
        


    def fit(self, p, q):

        """Create model, fit to `self.data`, and attach to `self.model` attribute.
        For assignment, also assigns adds metrics to `self.aic` and `self.bic`.

        Parameters
        ----------
        p : int
            Lag order of the symmetric innovation

        q : ind
            Lag order of lagged volatility

        Returns
        -------
        None
        """
        # Train Model, attach to `self.model`
        self.model = arch_model(self.data, p=p, q=q, rescale=False).fit(disp=0)
        

    def __clean_prediction(self, prediction):

        """Reformat model prediction to JSON.

        Parameters
        ----------
        prediction : pd.DataFrame
            Variance from a `ARCHModelForecast`

        Returns
        -------
        dict
            Forecast of volatility. Each key is date in ISO 8601 format.
            Each value is predicted volatility.
        """
        # Calculate forecast start date
        start = prediction.index[0] + pd.DateOffset(days=1)

        # Create date range
        prediction_dates = pd.bdate_range(start=start, periods=prediction.shape[1])

        # Create prediction index labels, ISO 8601 format
        prediction_index = [d.isoformat() for d in prediction_dates]


        # Extract predictions from DataFrame, get square root
        data=prediction.values.flatten() ** 0.5

        # Combine `data` and `prediction_index` into Series
        predicted_formatted=pd.Series(data, index=prediction_index)

        # Return Series as dictionary
        return predicted_formatted.to_dict()

    def predict_volatility(self, horizon):

        """Predict volatility using `self.model`

        Parameters
        ----------
        horizon : int
            Horizon of forecast, by default 5.

        Returns
        -------
        dict
            Forecast of volatility. Each key is date in ISO 8601 format.
            Each value is predicted volatility.
        """
        # Generate variance forecast from `self.model`
        prediction = self.model.forecast(horizon=horizon, reindex=False).variance

        # Format prediction with `self.__clean_prediction`
        prediction_formatted = self.__clean_prediction(prediction)

        # Return `prediction_formatted`
        return prediction_formatted

    def dump(self):

        """Save model to `self.model_directory` with timestamp.

        Returns
        -------
        str
            filepath where model was saved.
        """
        # Create timestamp in ISO format
        timestamp=pd.Timestamp.now().isoformat()
        # Save `self.model`
        filepath=os.path.join('prediction/models/', f"{timestamp}_{self.ticker}.pkl")
        filepath=filepath.replace(':','-')
        joblib.dump(self.model, filepath)

        # Return filepath
        return filepath

    def load(self):

        """Load most recent model in `self.model_directory` for `self.ticker`,
        attach to `self.model` attribute.
        """

        # Create pattern for glob search
        pattern=os.path.join(self.model_directory, f"*{self.ticker}.pkl")


        # Try to find path of latest model
        
        p=sorted(glob(pattern))
        if len(p)>0:
            model_path = p[-1]
            # Load model and attach to `self.model`
            self.model = joblib.load(model_path)
            return False
        else:
            return True
