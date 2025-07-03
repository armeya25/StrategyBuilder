from tkinter import messagebox
from lib.base import Base
############################################################################################################
class Builder(Base):
    def __init__(self):
        super().__init__()
        self.__selected_indicators = {}
        ## basic list for creating strategy
        self.__lists_for_strategy={
                                    'input_col_names'   : [],
                                    'input_col_str_list': [],
                                    'pre_col_names'     : [],
                                    'pre_col_str_list'  : [],
                                    'base_part'         : [],
                                    'special_part'      : [],
                                    'signal_buy'        : [],
                                    'signal_sell'       : []
                                }
        ## basic lists for charts
        self.__lists_for_chart={
                                    'lines'             : [],
                                    'subchart_lines'    : [],
                                    'subchart_histos'    : []
                                }
        self.__all_selected_params = {}
    ############################################################################################################
    def btn_windows_indicator_add(self, indicator, params:dict) -> None:
        __dict = {}
        var_name = ''
        full_indi_name = None
        ## if params are not empty
        if params != {}:
            for values in params.values():
                if var_name == '':
                    var_name = values
                else:
                    var_name = f'{var_name}_{values}'
            full_indi_name = f'{indicator}_{var_name}'
        else:
            full_indi_name = indicator
        
        if full_indi_name in self.__selected_indicators.keys():
            messagebox.showerror("Error", "Indicator already added")
            return
        __return_cols = self.indicators_all_values[self.indicators_names[indicator]]['indicators'][indicator]['return_cols']
        return_cols = []
        if isinstance(__return_cols, list):
            for col in __return_cols:
                col_x = f'{col}_{var_name}'
                return_cols.append(col_x)
                ## add in chart line if presents in that indicators lines list
                if col in self.indicators_all_values[self.indicators_names[indicator]]['indicators'][indicator]['charts']['lines']:
                    self.__lists_for_chart['lines'].append(col_x)
                if col in self.indicators_all_values[self.indicators_names[indicator]]['indicators'][indicator]['charts']['subchart_lines']:
                    self.__lists_for_chart['subchart_lines'].append(col_x)
                if col in self.indicators_all_values[self.indicators_names[indicator]]['indicators'][indicator]['charts']['subchart_histos']:
                    self.__lists_for_chart['subchart_histos'].append(col_x)
        else:
            if params != {}:
                return_cols = f'{__return_cols}_{var_name}'
            else:
                return_cols = __return_cols
            ## add in chart line if presents in that indicators lines list
            if __return_cols in self.indicators_all_values[self.indicators_names[indicator]]['indicators'][indicator]['charts']['lines']:
                self.__lists_for_chart['lines'].append(return_cols)
            if __return_cols in self.indicators_all_values[self.indicators_names[indicator]]['indicators'][indicator]['charts']['subchart_lines']:
                self.__lists_for_chart['subchart_lines'].append(return_cols)
            if __return_cols in self.indicators_all_values[self.indicators_names[indicator]]['indicators'][indicator]['charts']['subchart_histos']:
                self.__lists_for_chart['subchart_histos'].append(return_cols)

        __dict = {
                    'name'          : indicator,
                    'source'        : self.indicators_names[indicator],
                    'input_cols'    : self.indicators_all_values[self.indicators_names[indicator]]['indicators'][indicator]['inputs']['input_cols'],
                    'return_cols'   : return_cols,
                    'params'        : params
                }
        self.__selected_indicators[full_indi_name] = __dict
        ## add to all_cols
        if isinstance(return_cols, list):
            for col in return_cols:
                if col not in self.all_cols:
                    self.all_cols.append(col)
        else:
            if return_cols not in self.all_cols:
                self.all_cols.append(return_cols)
    ############################################################################################################
    def btn_windows_indicator_next_clicked(self) -> None:
        for key, value in self.__selected_indicators.items():
            #print(key, value)
            ## for input cols
            input_cols = value['input_cols']
            tmp_input_cols = ''
            if input_cols != 'None':
                ## if its list
                if isinstance(input_cols, list):
                    for col in input_cols:
                        if col not in self.input_col_list:
                            self.input_col_list.append(col)
                            colx = f'input_{col} = self.df.select("{col}").to_series()'
                            self.__lists_for_strategy['input_col_str_list'].append(colx)
                        tmp_input_cols = f'input_{col}, {tmp_input_cols}'
                ## if input_cols is single value
                else:
                    if input_cols not in self.input_col_list:
                        self.__lists_for_strategy['input_col_names'].append(input_cols)
                        col = f'input_{input_cols} = self.df.select("{input_cols}").to_series()'
                        self.__lists_for_strategy['input_col_str_list'].append(col)
                    tmp_input_cols = f'input_{input_cols}, {tmp_input_cols}'
            
            ## for return cols / pre_cols
            return_cols = value['return_cols']
            if return_cols != 'None':
                str_return_cols = ''
                _base_cols = []
                ## if its list
                if isinstance(return_cols, list):
                    for col in return_cols:
                        if col not in self.__lists_for_strategy['pre_col_names']:
                            self.__lists_for_strategy['pre_col_names'].append(col)
                            str_return_cols = f'{col}, {str_return_cols}'
                            _base_cols.append(f'{col} = {col},')
                    ## remove last , if any
                    str_return_cols = str_return_cols.removesuffix(', ')
                    ## source of indicator lib
                    str_return_cols = self.__source_of_indicator(str_return_cols, value['source'], value['name'], tmp_input_cols)
                    ## add params
                    for k, v in value['params'].items():
                        str_return_cols = f'{str_return_cols} {k}={v},'
                    ## remove last , if any
                    str_return_cols = str_return_cols.removesuffix(',')
                    str_return_cols = f'{str_return_cols})'
                    self.__lists_for_strategy['pre_col_str_list'].append(str_return_cols)
                    ## add to base part
                    self.__lists_for_strategy['base_part'] = self.__lists_for_strategy['base_part'] + _base_cols
                else:
                    if return_cols not in self.__lists_for_strategy['pre_col_names']:
                        self.__lists_for_strategy['pre_col_names'].append(return_cols)
                        str_return_cols = f'{key}, {str_return_cols}'
                        ## source of indicator lib
                        str_return_cols = self.__source_of_indicator(str_return_cols, value['source'], value['name'], tmp_input_cols)
                        if value['params'] != {}:
                            for k, v in value['params'].items():
                                str_return_cols = f'{str_return_cols} {k}={v},'
                            ## remove last , if any
                            str_return_cols = str_return_cols.removesuffix(',')
                            str_return_cols = f'{str_return_cols}),'
                        else:
                            str_return_cols = str_return_cols.removesuffix(', ')
                            str_return_cols = f'{str_return_cols}),'
                        self.__lists_for_strategy['base_part'].append(str_return_cols)
    ############################################################################################################
    def __source_of_indicator(self, key:str, source:str, name:str, input_cols:str) -> str:
        key = key.removesuffix(', ')
        if source == 'talib':
            return f'{key} = {source}.{name.upper()}({input_cols}'
        else:
            return f'{key} = {source}.{name.upper()}({input_cols}'
    ############################################################################################################
    def btn_windows_special_cases_add_clicked(self, params:dict) -> None:
        ## should not be empty
        var_name = f'{params['col']}_{params['cond']}_{params['value']}'
        ## add to all_cols list
        self.all_cols.append(var_name)
        ## add to special_part list
        special_part = f'{var_name} = pl.col("{params['col']}").{params['cond']}({params['value']})'
        self.__lists_for_strategy['special_part'].append(special_part)
        ## if its made from lines
        if params['col'] in self.__lists_for_chart['lines']:
            self.__lists_for_chart['lines'].append(var_name)
        ## if its made from subchart_lines
        elif params['col'] in self.__lists_for_chart['subchart_lines']:
            self.__lists_for_chart['subchart_lines'].append(var_name)
        ## if its made from subchart_histos
        elif params['col'] in self.__lists_for_chart['subchart_histos']:
            self.__lists_for_chart['subchart_histos'].append(var_name)
        else:
            ## for other cases
            self.__lists_for_chart['lines'].append(var_name)
    ############################################################################################################
    def btn_windows_strategy_add_clicked(self, params:dict) -> None:
        if params['buy_sell'] == 'buy':
            self.__lists_for_strategy['signal_buy'].append(self.__conditions(params))
        elif params['buy_sell'] == 'sell':
            self.__lists_for_strategy['signal_sell'].append(self.__conditions(params))
        else:
            raise ValueError("buy_sell should be buy or sell")
    ############################################################################################################
    def __conditions(self, params:dict) -> str:
        condition =  params['cond']
        col2 = None
        if params['col2'] != None:
            col2 = f'pl.col("{params['col2']}")'
        else:
            col2 = params['value1']

        if condition == "cross above":
            return f'((pl.col("{params['col1']}").shift() < {col2}.shift()) & (pl.col("{params['col1']}") > {col2})) &'
        elif condition == "cross below":
            return f'((pl.col("{params['col1']}").shift() > {col2}.shift()) & (pl.col("{params['col1']}") < {col2})) &'
        elif condition == "is_between":
            val1 = params['value1'] if params['value1'] != None else f'pl.col("{params['optional_col1']}")'
            val2 = params['value2'] if params['value2'] != None else f'pl.col("{params['optional_col2']}")'
            return f'((pl.col("{params['col1']}").is_between({val1}, {val2}))) &'
        elif condition == ">":
            return f'((pl.col("{params['col1']}") > {col2})) &'
        elif condition == "<":
            return f'((pl.col("{params['col1']}") < {col2})) &'
        elif condition == "==":
            return f'((pl.col("{params['col1']}") == {col2})) &'
        elif condition == "!=":
            return f'((pl.col("{params['col1']}") != {col2})) &'
        elif condition == ">=":
            return f'((pl.col("{params['col1']}") >= {col2})) &'
        elif condition == "<=":
            return f'((pl.col("{params['col1']}") <= {col2})) &'
        else:
            raise NotImplementedError("condition not implemented")
    ############################################################################################################
    def btn_strategy_window_finalise_clicked(self) -> None:
        ## selected indicators should not be empty
        with open(self.output_file, "w") as f:
            f.write("import random\n")
            f.write("import polars as pl\n")
            #f.write(f"import {self.indicators_names}\n")
            ## write indicators libraries that will be imported
            for indicator_lib in self.indicators_lib:
                if indicator_lib == 'custom':
                    f.write("from lib.indicators.custom import custom\n")
                else:
                    f.write(f"import {indicator_lib}\n")
            
            if self.charting_lib == 'lightweight_charts':
                f.write("from lightweight_charts import Chart\n")
            elif self.charting_lib == 'finplot':
                f.write("import finplot as fplt\n")
            
            f.write('\nclass Strategy:\n')
            f.write('\tdef __init__(self, df:pl.DataFrame) -> None:\n')
            f.write('\t\tself.df = df\n')
            f.write('\t\tself.__colors = []\n')
            
            ######################################
            ## strategy created from here onwards ##
            ######################################
            f.write('\tdef calculate(self):\n')
            ## write input cols
            if self.__lists_for_strategy['input_col_str_list']:
                for col in self.__lists_for_strategy['input_col_str_list']:
                    f.write(f'\t\t{col}\n')
            ## write pre_cols in there any
            if self.__lists_for_strategy['pre_col_str_list']:
                for col in self.__lists_for_strategy['pre_col_str_list']:
                    f.write(f'\t\t{col}\n')
            ## write base part
            if self.__lists_for_strategy['base_part']:
                f.write('\t\tself.df=(\n\t\t\t\t\tself.df\n')
                f.write("\t\t\t\t\t## Base Part\n")
                f.write('\t\t\t\t\t.with_columns\n\t\t\t\t\t(\n')
                for col in self.__lists_for_strategy['base_part']:
                    f.write(f'\t\t\t\t\t\t{col}\n')
                f.write('\t\t\t\t\t)\n')        ## close with_columns
            else:
                f.write('\t\tself.df=(\n\t\t\t\t\tself.df\n')

            ## write special part
            if self.__lists_for_strategy['special_part']:
                f.write('\t\t\t\t\t## Special Part\n')
                f.write('\t\t\t\t\t.with_columns\n\t\t\t\t\t(\n')
                for col in self.__lists_for_strategy['special_part']:
                    f.write(f'\t\t\t\t\t\t{col},\n')
                f.write('\t\t\t\t\t)\n')        ## close with_columns
            
            ## write signal part
            if self.__lists_for_strategy['signal_buy'] or self.__lists_for_strategy['signal_sell']:
                
                f.write('\t\t\t\t\t ## Signal Part\n')
                f.write('\t\t\t\t\t.with_columns\n\t\t\t\t\t(\n')
                ## if there is buy part
                if self.__lists_for_strategy['signal_buy']:
                    f.write('\t\t\t\t\t\t## BUY SIGNAL\n')
                    f.write('\t\t\t\t\t\tpl.when\n\t\t\t\t\t\t(\n')
                    col = self.__signal_list_to_str(self.__lists_for_strategy['signal_buy'])
                    for c in col:
                        f.write(c)
                    f.write('\t\t\t\t\t\t)\n')    ## close when condition
                    ##if there is no sell part
                    if not self.__lists_for_strategy['signal_sell']:
                        f.write('\t\t\t\t\t\t.then(pl.lit("buy"))\n')
                        f.write('\t\t\t\t\t\t.alias("signal")\n')
                    else:
                        f.write('\t\t\t\t\t\t.then(pl.lit("buy"))\n')

                ## if there is sell part
                if self.__lists_for_strategy['signal_sell']:
                    f.write('\t\t\t\t\t\t## SELL SIGNAL\n')
                    f.write('\t\t\t\t\t\t.when\n\t\t\t\t\t\t(\n')
                    col = self.__signal_list_to_str(self.__lists_for_strategy['signal_sell'])
                    for c in col:
                        f.write(c)
                    f.write('\t\t\t\t\t\t)\n')    ## close when conditon
                    f.write('\t\t\t\t\t\t.then(pl.lit("sell"))\n')
                    f.write('\t\t\t\t\t\t.alias("signal")\n')

                f.write('\t\t\t\t\t)\n')        ## close with_columns
            ## write this at last part
            f.write('\t\t\t\t)\n')          ## closes self.df
            f.write(f'\t{self.hashtag*5}\n')
        f.close()

        ############################
        ## for charting libraries ##
        ############################
        ## if its lightweight charts
        if self.charting_lib == 'lightweight_charts':
            self.for_lightweight_charts()
        ## if its finplot
        elif self.charting_lib == 'finplot':
            self.for_finplot()
        
        ###############################
        ## write for testing purpose ##
        ###############################
        with open(self.output_file, "a") as f:
            f.write('df = pl.read_csv("sbin.csv")\n')
            f.write('s = Strategy(df)\n')
            f.write('s.calculate()\n')
            f.write('s.plot()')
        f.close()
    ############################################################################################################
    def __signal_list_to_str(self, signal_list:list) -> str:
        for idx, col in enumerate(signal_list):
            if idx == len(signal_list) - 1:
                col = col.removesuffix(' &')
                col = col.removesuffix(' |')
                yield f'\t\t\t\t\t\t\t{col}\n'
            else:
                yield f'\t\t\t\t\t\t\t{col}\n'
    ############################################################################################################
    def for_lightweight_charts(self):
        with open(self.output_file, "a") as f:
            ######################################
            ## charts created from here onwards ##
            ######################################
            ## random color generator function
            f.write('\tdef __generate_random_color(self):\n')
            f.write('\t\tclr1 = random.randint(0, 255)\n\t\tclr2 = random.randint(0, 255)\n\t\tclr3 = random.randint(0, 255)\n')
            f.write('\t\tclr = "rgba(" + str(clr1) + "," + str(clr2) + "," + str(clr3) + ", 1)"\n')
            f.write('\t\tif clr not in self.__colors:\n\t\t\tself.__colors.append(clr)\n\t\t\treturn clr\n')
            f.write('\t\tself.__generate_random_color()\n')
            f.write(f'\t{self.hashtag*5}\n')

            ## charting function
            f.write('\tdef plot(self):\n')
            ## should i draw subchart or not
            if self.__lists_for_chart['subchart_lines'] or self.__lists_for_chart['subchart_histos']:
                ## main chart
                f.write('\t\tchart = Chart(inner_width=1, inner_height=0.6)\n')
                ## subchart
                f.write('\t\tsubchart = chart.create_subchart(height=0.4, width=1, sync=True)\n')
                f.write('\t\tsubchart.legend(True)\n')
            else:
                ## if not subchart present
                f.write('\t\tchart = Chart()\n')
            f.write('\t\tchart.legend(True)\n')
            f.write('\t\tchart.set(self.df.select("date", "open", "high", "low", "close").to_pandas())\n')
            ## write lines and their respective dfs
            ## if available
            if self.__lists_for_chart['lines']:
                f.write(f'\n\t\t## lines setup\n')
                for line in self.__lists_for_chart['lines']:
                    line_name = f'{line}_line'
                    f.write(f'\t\t{line_name} = chart.create_line(name="{line}", width=1, price_label=False, price_line=False, color=self.__generate_random_color())\n')
                    f.write(f'\t\t{line_name}.set(self.df.select("date", "{line}").to_pandas())\n')
            
            ## if there is subcharts available to plot
            if self.__lists_for_chart['subchart_lines'] or self.__lists_for_chart['subchart_histos']:
                ## if there are lines in subchart
                if self.__lists_for_chart['subchart_lines']:
                    f.write(f'\n\t\t## subchart lines setup\n')
                    for line in self.__lists_for_chart['subchart_lines']:
                        line_name = f'{line}_line'
                        f.write(f'\t\t{line_name} = subchart.create_line(name="{line}", price_label=False, price_line=False, color=self.__generate_random_color())\n')
                        f.write(f'\t\t{line_name}.set(self.df.select("date", "{line}").to_pandas())\n')
                ## if there are histograms in subchart
                if self.__lists_for_chart['subchart_histos']:
                    f.write(f'\n\t\t## subchart histograms setup\n')
                    for histo in self.__lists_for_chart['subchart_histos']:
                        histo_name = f'{histo}_histo'
                        f.write(f'\t\t{histo_name} = subchart.create_histogram(name="{histo}", price_label=False, price_line=False, color=self.__generate_random_color())\n')
                        f.write(f'\t\t{histo_name}.set(self.df.select("date", "{histo}").to_pandas())\n')
            
            ## mark signals if available
            f.write('\n\t\t## mark signals if available\n')
            f.write('\t\tsignal = self.df.filter(pl.col("signal").is_not_null()).select("date", "signal")\n')
            f.write('\t\tfor f in signal.iter_slices(1):\n')
            f.write('\t\t\tif f.item(0, "signal") == "buy":\n')
            f.write('\t\t\t\tchart.marker(time=f.item(0, "date"),position="below", color="green", shape="arrow_up", text="BUY")\n')
            f.write('\t\t\telse:\n')
            f.write('\t\t\t\tchart.marker(time=f.item(0, "date"),position="above", color="red", shape="arrow_down", text="SELL")\n')
		
            ## show plots
            f.write('\n\t\tchart.show(block=True)\n\n')
            f.write(f'\t{self.hashtag*5}\n')
    ############################################################################################################