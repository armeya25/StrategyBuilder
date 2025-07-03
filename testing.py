import random
import polars as pl
import talib
from lightweight_charts import Chart

class Strategy:
	def __init__(self, df:pl.DataFrame) -> None:
		self.df = df
		self.__colors = []
	def calculate(self):
		self.df=(
					self.df
				)
	##############################################################################################################
	def __generate_random_color(self):
		clr1 = random.randint(0, 255)
		clr2 = random.randint(0, 255)
		clr3 = random.randint(0, 255)
		clr = "rgba(" + str(clr1) + "," + str(clr2) + "," + str(clr3) + ", 1)"
		if clr not in self.__colors:
			self.__colors.append(clr)
			return clr
		self.__generate_random_color()
	##############################################################################################################
	def plot(self):
		chart = Chart()
		chart.legend(True)
		chart.set(self.df.select("date", "open", "high", "low", "close").to_pandas())

		## mark signals if available
		signal = self.df.filter(pl.col("signal").is_not_null()).select("date", "signal")
		for f in signal.iter_slices(1):
			if f.item(0, "signal") == "buy":
				chart.marker(time=f.item(0, "date"),position="below", color="green", shape="arrow_up", text="BUY")
			else:
				chart.marker(time=f.item(0, "date"),position="above", color="red", shape="arrow_down", text="SELL")

		chart.show(block=True)

	##############################################################################################################
df = pl.read_csv("sbin.csv")
s = Strategy(df)
s.calculate()
s.plot()