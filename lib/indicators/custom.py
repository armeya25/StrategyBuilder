import polars as pl
############################################################################################################
class custom:
    ############################################################################################################
    @staticmethod
    def ICHIMOKU(high:pl.Series, low:pl.Series, close:pl.Series, timeperiod: int = 9, fastperiod: int = 26, slowperiod: int = 52) -> pl.DataFrame:
        df = pl.DataFrame({'high': high, 'low': low, 'close': close})
        df =(
                df.with_columns
                (
                # Calculate Tenkan-sen (Conversion Line)
                tenkan_sen = (pl.col('high').rolling_max(timeperiod) + pl.col('low').rolling_min(timeperiod)) / 2,
                # Calculate Kijun-sen (Base Line)
                kijun_sen = (pl.col('high').rolling_max(fastperiod) + pl.col('low').rolling_min(fastperiod)) / 2,
                # Calculate Chikou Span (Lagging Span)
                chikou_span = pl.col('close').shift(-26),
            )
            .with_columns
            (
                # Calculate Leading Span A
                leading_span_a = ((pl.col('tenkan_sen') + pl.col('kijun_sen')) / 2).shift(26),
                # Calculate Leading Span B
                leading_span_b = (pl.col('high').rolling_max(slowperiod) + pl.col('low').rolling_min(slowperiod)) / 2
            )
        ).select(['tenkan_sen', 'kijun_sen', 'chikou_span', 'leading_span_a', 'leading_span_b'])
        return df['tenkan_sen'], df['kijun_sen'], df['chikou_span'], df['leading_span_a'], df['leading_span_b']
    ############################################################################################################
