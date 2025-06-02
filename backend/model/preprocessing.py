from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
import pandas as pd


class Preprocessor(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        self.num_cols = ['CreditScore', 'Age', 'Tenure', 'Balance',
                         'NumOfProducts', 'EstimatedSalary']
        self.cat_cols = ['Geography']

    def _clean_data(self, X):
        df = X.copy()

        df = df.drop(columns=['RowNumber', 'CustomerId', 'Surname'], errors='ignore')
        df['Geography'] = df['Geography'].fillna(df['Geography'].mode()[0])
        df['Age'] = df['Age'].fillna(df['Age'].median())

        df = df.dropna()
        df = df.drop_duplicates()

        df['Gender'] = df['Gender'].map({'Male': 0, 'Female': 1})

        return df

    def fit(self, X, y=None):
        df = self._clean_data(X)
        self.scaler.fit(df[self.num_cols])
        self.ohe.fit(df[self.cat_cols])
        return self

    def transform(self, X):
        df = self._clean_data(X)

        geo_encoded = self.ohe.transform(df[self.cat_cols])
        geo_df = pd.DataFrame(
            geo_encoded,
            columns=self.ohe.get_feature_names_out(self.cat_cols),
            index=df.index
        )

        df_scaled = self.scaler.transform(df[self.num_cols])
        df_scaled = pd.DataFrame(df_scaled, columns=self.num_cols, index=df.index)

        final_df = pd.concat([df_scaled, geo_df, df['Gender']], axis=1)

        return final_df
