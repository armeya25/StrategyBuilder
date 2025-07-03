import tkinter as tk
from tkinter import ttk, messagebox
import toml
from lib.builder import Builder

############################################################################################################
class Main(Builder):
    def __init__(self):
        super().__init__()
        
        ## variable for comboboxes stored as dict here
        self.__combo_vars = {}

        ## checkboxes variables
        self.__checkbox_vars = {}

        ## selected indicators list
        self.__selected_indicator_list = []

         ## select indicators window frame parameter label
        self.__indicator_window_frame_parameter_label = []
        ## entry names
        self.__entry_names_dict = {}
        ## get values from entry boxes
        self.__entry_input_var_dict = {}
        ## enabled entries for each indicator always changes with indicator
        self.__windows_indicator_enabled_entries = []
    ############################################################################################################
    def main(self):
        self.__root = tk.Tk()
        self.__root.title("Strategy Builder")

        ## create frame
        self.__window_main = ttk.Frame(self.__root, padding="10")
        self.__window_main.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ## charting libraries frame
        charting_frame = ttk.LabelFrame(self.__window_main, text="Charting Libraries")
        charting_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky='ew')
        charting_frame.columnconfigure(1, weight=1)

        ## create label and combobox
        ttk.Label(charting_frame, text="charting libraries", foreground='blue').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.__combo_vars['charting_lib'] = tk.StringVar(value=self.base_configs['select_libs']['charts'][0])
        self.__window_main_combo_charting_lib = ttk.Combobox(charting_frame, textvariable=self.__combo_vars['charting_lib'])
        self.__window_main_combo_charting_lib['values'] = self.base_configs['select_libs']['charts']
        self.__window_main_combo_charting_lib.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        

        ## indicator libraries frame
        indicator_frame = ttk.LabelFrame(self.__window_main, text="Indicator Libraries")
        indicator_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky='ew')
        indicator_frame.columnconfigure(0, weight=1)

        ## create checkboxes
        for idx, libs in enumerate(self.base_configs['select_libs']['indicator_libs']):
            self.__checkbox_vars[libs] = tk.BooleanVar()
            if libs == 'talib':
                self.__checkbox_vars[libs].set(True)
            ttk.Checkbutton(indicator_frame, text=libs, variable=self.__checkbox_vars[libs]).pack(anchor='w', padx=5, pady=2)
        

        ## buttons
        ## next button
        tk.Button(self.__window_main, text="Next", command=self.__btn_main_next_clicked, foreground='green').grid(row=self.__checkbox_vars.__len__()+2, column=1, columnspan=1, pady=10, sticky='e')
        
        self.__root.mainloop()
    ############################################################################################################
    def __btn_main_next_clicked(self):
        if not any(value.get() for value in self.__checkbox_vars.values()):
            messagebox.showerror("No indicators selected", "Please select at least one indicator library")
            return
        ## set which charting lib to use
        self.charting_lib = self.__combo_vars['charting_lib'].get()

        ## get all selected indicators names
        for key, value in self.__checkbox_vars.items():
            if value.get():
                ## add to selected indicators libraries list
                self.indicators_lib.append(key)
                if not key in self.__selected_indicator_list:
                    self.__selected_indicator_list.append(key)
        
        ## load configs for selected indicators
        for indicator_lib in self.__selected_indicator_list:
            self.indicators_all_values[indicator_lib] = toml.load(f"{self.config_location}/{indicator_lib}_configs.toml")
            for indicator_name in self.indicators_all_values[indicator_lib]['indicators'].keys():
                self.indicators_names[indicator_name] = indicator_lib
        
        ## minimise root window
        self.__root.iconify()
        
        ## create select indicators window
        self.__windows_indicator()
    ############################################################################################################
    def __windows_indicator(self):
        self.__windows_indicator = tk.Toplevel(self.__root)
        self.__windows_indicator.title("Select Indicators")
        
        ## add frame
        self.__windows_indicator_frame = ttk.Frame(self.__windows_indicator, padding="10")
        self.__windows_indicator_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ## first row
        ## add labels
        ttk.Label(self.__windows_indicator_frame, text="Select Indicator").grid(row=0, column=0, padx=5, pady=5)
        ## add combobox and changes callback
        self.__combo_vars['windows_indicator_combo_var'] = tk.StringVar()
        self.__windows_indicator_combo_indicators = ttk.Combobox(self.__windows_indicator_frame, textvariable=self.__combo_vars['windows_indicator_combo_var'])
        self.__windows_indicator_combo_indicators['values'] = sorted(list(self.indicators_names.keys()))
        self.__windows_indicator_combo_indicators.grid(row=0, column=1, padx=5, pady=5)
        self.__windows_indicator_combo_indicators.bind('<<ComboboxSelected>>', self.__cmb_windows_indicator_combo_changed)

        ## configure input variables to add in gui
        for values in self.indicators_all_values.values():
            for value in values['indicators'].values():
                for param_name in value['inputs']:
                    if param_name != 'input_cols':
                        if param_name not in self.__indicator_window_frame_parameter_label:
                            self.__indicator_window_frame_parameter_label.append(param_name)
        
        ## set labels and entry boxes
        for idx, param_name in enumerate(self.__indicator_window_frame_parameter_label):
            ttk.Label(self.__windows_indicator_frame, text=param_name, justify=tk.LEFT).grid(row=idx+1, column=0, padx=5, pady=5)
            entry_names = f'{param_name}_entry'
            self.__entry_names_dict[entry_names] = ttk.Entry(self.__windows_indicator_frame, justify=tk.LEFT, width=10, validate='key')#, validatecommand=vcmd, state=tk.DISABLED)
            self.__entry_names_dict[entry_names].grid(row=idx+1, column=1, padx=5, pady=5)
            ## set variable names used for setting values
            self.__entry_input_var_dict[param_name] = tk.StringVar()
            self.__entry_names_dict[entry_names].config(state=tk.DISABLED, textvariable=self.__entry_input_var_dict[param_name])

        ## group buttons
        buttons_frame = ttk.Frame(self.__windows_indicator_frame, padding="5")
        buttons_frame.grid(row=self.__indicator_window_frame_parameter_label.__len__()+1, column=0, columnspan=2, pady=5)
        
        # Create a frame for each button with padding
        add_button_frame = ttk.Frame(buttons_frame, padding="5")
        next_button_frame = ttk.Frame(buttons_frame, padding="5")
        
        # Pack the button frames with padding
        add_button_frame.pack(side=tk.LEFT, padx=5)
        next_button_frame.pack(side=tk.LEFT, padx=5)
        
        # Add buttons to their respective frames
        tk.Button(add_button_frame, text="Add", command=self.__btn_windows_indicator_add_clicked).pack()
        tk.Button(next_button_frame, text="Next", command=self.__btn_windows_indicator_next_clicked).pack()
    ############################################################################################################
    def __cmb_windows_indicator_combo_changed(self, *args):
        selected_indicator = self.__combo_vars['windows_indicator_combo_var'].get()
        if selected_indicator:
            # Get the inputs for this indicator from configs
            lib_name = self.indicators_names[selected_indicator]
            inputs = self.indicators_all_values[lib_name]['indicators'][selected_indicator]['inputs']

            self.__windows_indicator_enabled_entries = []
            
            ## select entry boxes and clear them
            for key in self.__entry_names_dict.keys():
                self.__entry_names_dict[key].config(state=tk.DISABLED)
                self.__entry_names_dict[key].delete(0, tk.END)
            
            ## enable and set values for required inputs
            for key, value in inputs.items():
                if key != 'input_cols':
                    entry_names = f'{key}_entry'
                    self.__entry_names_dict[entry_names].config(state=tk.NORMAL)
                    self.__entry_input_var_dict[key].set(str(value))
                    self.__windows_indicator_enabled_entries.append(entry_names)
    ############################################################################################################
    def __btn_windows_indicator_add_clicked(self):
        """Handle the Add button click"""
        selected_indicator = self.__combo_vars['windows_indicator_combo_var'].get()
        if not selected_indicator:
            messagebox.showwarning("Warning", "Please select an indicator")
            return
        ## get values for required inputs
        params = {}
        for entry_name in self.__windows_indicator_enabled_entries:
            ## get values and names from entry boxes
            params[entry_name.replace('_entry', '')] = self.__entry_input_var_dict[entry_name.replace('_entry', '')].get()
            ## clear entry boxes
            self.__entry_names_dict[entry_name].delete(0, tk.END)
            ## disable entry boxes
            self.__entry_names_dict[entry_name].config(state=tk.DISABLED)
        
        ## call add indicators from builder class
        self.btn_windows_indicator_add(selected_indicator, params)
        
        ## clear indicator combobox
        self.__combo_vars['windows_indicator_combo_var'].set('')
    ############################################################################################################
    def __btn_windows_indicator_next_clicked(self):
        ## minimise root window
        self.__windows_indicator.destroy()
        ## call this function from builder class
        self.btn_windows_indicator_next_clicked()
        ## create special cases window
        self.__windows_special_cases()
    ############################################################################################################
    def __windows_special_cases(self):
        self.__windows_special_cases = tk.Toplevel(self.__root)
        self.__windows_special_cases.title("Select Special Cases")
        
        ## add frame
        self.__windows_special_cases_frame = ttk.Frame(self.__windows_special_cases, padding="10")
        self.__windows_special_cases_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ## special cases frame
        special_cases_inner_frame = ttk.Frame(self.__windows_special_cases_frame)
        special_cases_inner_frame.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        special_cases_inner_frame.columnconfigure(1, weight=1)

        ## add labels and combobox
        ttk.Label(special_cases_inner_frame, text="Select Column").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.__combo_vars['windows_special_cases_combo_cols_var'] = tk.StringVar()
        self.__windows_special_cases_combo_cols = ttk.Combobox(special_cases_inner_frame, textvariable=self.__combo_vars['windows_special_cases_combo_cols_var'])
        self.__windows_special_cases_combo_cols['values'] = self.all_cols
        self.__windows_special_cases_combo_cols.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.__windows_special_cases_combo_cols.bind('<<ComboboxSelected>>', self.__cmb_windows_special_cases_cols_changed)

        ## add labels and combobox
        ttk.Label(special_cases_inner_frame, text="Select Condition").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.__combo_vars['window_special_cases_cond_var'] = tk.StringVar()
        self.__windows_special_cases_combo_cond = ttk.Combobox(special_cases_inner_frame, textvariable=self.__combo_vars['window_special_cases_cond_var'], state=tk.DISABLED, width=15)
        self.__windows_special_cases_combo_cond['values'] = self.base_configs['conditions']['special']
        self.__windows_special_cases_combo_cond.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.__windows_special_cases_combo_cond.bind('<<ComboboxSelected>>', self.__cmb_windows_special_cases_cond_changed)

        ## add labels and entry
        ttk.Label(special_cases_inner_frame, text="Enter Value").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        
        self.__entry_input_var_dict['special_value'] = tk.StringVar()
        #vcmd = (self.root.register(self.__validate_int), '%P')
        self.__windows_special_cases_entry = ttk.Entry(special_cases_inner_frame, validate='key', width=10)
        self.__windows_special_cases_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.__windows_special_cases_entry.config(textvariable=self.__entry_input_var_dict['special_value'], state=tk.DISABLED)
        
        ## buttons frame
        buttons_frame = ttk.Frame(self.__windows_special_cases_frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ## add buttons
        tk.Button(buttons_frame, text="Add", command=self.__btn_windows_special_cases_add_clicked).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Next", command=self.__btn_windows_special_cases_next_clicked).pack(side='left', padx=5)
    ############################################################################################################
    def __cmb_windows_special_cases_cols_changed(self, *agrs):
        selected_cols = self.__combo_vars['windows_special_cases_combo_cols_var'].get()
        if selected_cols in ['None', '']:
            self.__windows_special_cases_combo_cond.config(state=tk.DISABLED)
        else:
            self.__windows_special_cases_combo_cond.config(state=tk.NORMAL)
    ############################################################################################################
    def __cmb_windows_special_cases_cond_changed(self, *args):
        selected_cond = self.__combo_vars['window_special_cases_cond_var'].get()
        if selected_cond in ['None', '']:
            self.__windows_special_cases_entry.config(state=tk.DISABLED)
        else:
            self.__windows_special_cases_entry.config(state=tk.NORMAL)
    ############################################################################################################
    def __btn_windows_special_cases_add_clicked(self):
        cols = self.__combo_vars['windows_special_cases_combo_cols_var'].get()
        cond = self.__combo_vars['window_special_cases_cond_var'].get()
        value = self.__entry_input_var_dict['special_value'].get()

        ## disable comboboxes
        self.__windows_special_cases_combo_cond.config(state=tk.DISABLED)
        self.__windows_special_cases_entry.config(state=tk.DISABLED)

        self.__entry_input_var_dict['special_value'].set('')
        if value == '':
            messagebox.showerror("Error", "Please enter a value")
            return
        params={
                'col' : cols,
                'cond': cond,
                'value': value
            }

        self.__combo_vars['window_special_cases_cond_var'].set('')
        self.__combo_vars['windows_special_cases_combo_cols_var'].set('')
        self.__entry_input_var_dict['special_value'].set('')
        self.btn_windows_special_cases_add_clicked(params)
    ############################################################################################################
    def __btn_windows_special_cases_next_clicked(self):
        ## minimise special window
        self.__windows_special_cases.destroy()
        ## open strategy window
        self.__windows_strategy()
    ############################################################################################################
    def __windows_strategy(self):
        self.__strategy_window = tk.Toplevel(self.__root)
        self.__strategy_window.title("Create Strategy")
        
        ## add frame
        strategy_window_frame = ttk.Frame(self.__strategy_window, padding="10")
        strategy_window_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ## condition 1 frame
        cond1_frame = ttk.LabelFrame(strategy_window_frame, text="Condition 1")
        cond1_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky='ew')
        cond1_frame.columnconfigure(1, weight=1)

        ## column 1 selection
        ttk.Label(cond1_frame, text="Column 1").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.__combo_vars['strategy_window_combo_col1_var'] = tk.StringVar()
        self.__strategy_window_combo_col1 = ttk.Combobox(cond1_frame, textvariable=self.__combo_vars['strategy_window_combo_col1_var'], width=30)
        self.__strategy_window_combo_col1['values'] = self.all_cols
        self.__strategy_window_combo_col1.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.__strategy_window_combo_col1.bind('<<ComboboxSelected>>', self.__cmb_strategy_col1_changed)
        ## conditions
        ttk.Label(cond1_frame, text="Conditions").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.__combo_vars['strategy_window_combo_cond_var'] = tk.StringVar()
        self.__strategy_window_combo_cond1 = ttk.Combobox(cond1_frame, textvariable=self.__combo_vars['strategy_window_combo_cond_var'], width=15, state=tk.DISABLED)
        self.__strategy_window_combo_cond1['values'] = self.base_configs['conditions']['conditions']
        self.__strategy_window_combo_cond1.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.__strategy_window_combo_cond1.bind('<<ComboboxSelected>>', self.__cmb_strategy_cond1_changed)
        
        ## value entries frame
        value_frame = ttk.LabelFrame(strategy_window_frame, text="Values")
        value_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky='ew')
        value_frame.columnconfigure(1, weight=1)
        ## value 1
        ttk.Label(value_frame, text="Value 1").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.__strategy_window_entry_value1 = ttk.Entry(value_frame, width=10)
        self.__strategy_window_entry_value1.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.__entry_input_var_dict['strategy_value1'] = tk.StringVar()
        self.__strategy_window_entry_value1.config(textvariable=self.__entry_input_var_dict['strategy_value1'], state=tk.DISABLED)
        ## or 
        ## optinal column 1
        ttk.Label(value_frame, text="Or").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.__combo_vars['strategy_window_combo_optional_col1_var'] = tk.StringVar()
        self.__strategy_window_combo_optional_col1 = ttk.Combobox(value_frame, textvariable=self.__combo_vars['strategy_window_combo_optional_col1_var'], width=30, state=tk.DISABLED)
        self.__strategy_window_combo_optional_col1['values'] = self.all_cols
        self.__strategy_window_combo_optional_col1.grid(row=0, column=3, padx=5, pady=5, sticky='w')

        ## value 2
        ttk.Label(value_frame, text="Value 2").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.__strategy_window_entry_value2 = ttk.Entry(value_frame, width=10)
        self.__strategy_window_entry_value2.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.__entry_input_var_dict['strategy_value2'] = tk.StringVar()
        self.__strategy_window_entry_value2.config(textvariable=self.__entry_input_var_dict['strategy_value2'], state=tk.DISABLED)
        ## or 
        ## optinal column 2
        ttk.Label(value_frame, text="Or").grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.__combo_vars['strategy_window_combo_optional_col2_var'] = tk.StringVar()
        self.__strategy_window_combo_optional_col2 = ttk.Combobox(value_frame, textvariable=self.__combo_vars['strategy_window_combo_optional_col2_var'], width=30, state=tk.DISABLED)
        self.__strategy_window_combo_optional_col2['values'] = self.all_cols
        self.__strategy_window_combo_optional_col2.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        
        ## condition 2 frame
        cond2_frame = ttk.LabelFrame(strategy_window_frame, text="Condition 2")
        cond2_frame.grid(row=4, column=0, columnspan=2, pady=5, sticky='ew')
        cond2_frame.columnconfigure(1, weight=1)

        ## column 2 selection
        ttk.Label(cond2_frame, text="Column 2").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.__combo_vars['strategy_window_combo_col2_var'] = tk.StringVar()
        self.__entry_input_var_dict['strategy_value3'] = tk.StringVar()
        self.__strategy_window_combo_col2 = ttk.Combobox(cond2_frame, textvariable=self.__combo_vars['strategy_window_combo_col2_var'], width=30)
        self.__strategy_window_combo_col2['values'] = self.all_cols
        self.__strategy_window_combo_col2.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        ## buy/sell frame
        buy_sell_frame = ttk.LabelFrame(strategy_window_frame, text="Buy/Sell")
        buy_sell_frame.grid(row=5, column=0, columnspan=2, pady=5, sticky='ew')
        buy_sell_frame.columnconfigure(1, weight=1)

        ## buy sell selection
        ttk.Label(buy_sell_frame, text="Buy/Sell").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.__combo_vars['strategy_window_buy_sell_var'] = tk.StringVar()
        self.__strategy_window_buy_sell = ttk.Combobox(buy_sell_frame, width=15, textvariable=self.__combo_vars['strategy_window_buy_sell_var'])
        self.__strategy_window_buy_sell['values'] = ['None', 'buy', 'sell']
        self.__strategy_window_buy_sell.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        ## seventh row
        ## buttons frame
        buttons_frame = ttk.Frame(strategy_window_frame)
        buttons_frame.grid(row=6, column=0, columnspan=2, pady=5)
        
        ## add buttons
        ttk.Button(buttons_frame, text='Add', command=self.__btn_window_strategy_add_clicked).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text='Finalise', command=self.__btn_window_strategy_finalise_clicked).pack(side='left', padx=5)
    ############################################################################################################
    def __cmb_strategy_col1_changed(self, *args):
        col1_var = self.__combo_vars['strategy_window_combo_col1_var'].get()
        if col1_var not in ['', "None"]:
            # Enable the condition combobox when a column is selected
            self.__strategy_window_combo_cond1.configure(state=tk.NORMAL)
        else:
            # Disable the condition combobox when no column is selected
            self.__strategy_window_combo_cond1.configure(state=tk.DISABLED)
    ############################################################################################################
    def __cmb_strategy_cond1_changed(self, *args):
        cond_var = self.__combo_vars['strategy_window_combo_cond_var'].get()
        
        if cond_var not in ['', "None"]:
            # Enable the value entry when a condition is selected
            self.__strategy_window_entry_value1.configure(state=tk.NORMAL)
            self.__strategy_window_combo_optional_col1.configure(state=tk.NORMAL)
            if cond_var == 'is_between':
                self.__strategy_window_entry_value2.configure(state=tk.NORMAL)
                self.__strategy_window_combo_optional_col2.configure(state=tk.NORMAL)
            else:
                self.__strategy_window_entry_value2.configure(state=tk.DISABLED)
                self.__strategy_window_combo_optional_col2.configure(state=tk.DISABLED)
        else:
            # Disable the value entry when no condition is selected
            self.__strategy_window_entry_value1.configure(state=tk.DISABLED)
            self.__strategy_window_entry_value2.configure(state=tk.DISABLED)
            self.__strategy_window_combo_optional_col1.configure(state=tk.DISABLED)
    ############################################################################################################
    def __btn_window_strategy_add_clicked(self):
        condition = self.__combo_vars['strategy_window_combo_cond_var'].get()

        value1 = self.__entry_input_var_dict['strategy_value1'].get()
        optional_col1 = self.__combo_vars['strategy_window_combo_optional_col1_var'].get()
        ## if value1 and optional_col1 are not empty at same time
        if value1 != '' and optional_col1 not in ['', 'None']:
            messagebox.showerror("Error", "can't add both value1 and optional col 1")
            return
        
        value2 = self.__entry_input_var_dict['strategy_value2'].get()
        optional_col2 = self.__combo_vars['strategy_window_combo_optional_col2_var'].get()
        if value2 != '' and optional_col2 not in ['', 'None']:
            messagebox.showerror("Error", "can't add both value2 and optional col 2")
            return
        
        col2 = self.__combo_vars['strategy_window_combo_col2_var'].get()
        if col2 in ['', 'None']:
            ## value1 or optional_col1 should not be empty
            if value1 in ['', 'None'] and optional_col1 in ['', 'None']:
                messagebox.showerror("Error", "col2 cannot be empty")
                return
        
        buy_sell = self.__combo_vars['strategy_window_buy_sell_var'].get()
        if buy_sell in ['', 'None']:
            messagebox.showerror("Error", "buy/sell cannot be empty")
            return
            
        params = {
            'col1': self.__combo_vars['strategy_window_combo_col1_var'].get(),
            'cond': condition,
            'value1': value1 if value1 not in ['', 'None'] else None,
            'optional_col1': optional_col1 if optional_col1 not in ['', 'None'] else None,
            'value2': value2 if value2 not in ['', 'None'] else None,
            'optional_col2': optional_col2 if optional_col2 not in ['', 'None'] else None,
            'col2': col2 if col2 not in ['', 'None'] else None,
            'buy_sell': buy_sell
        }
        self.btn_windows_strategy_add_clicked(params)
        ## clear all
        self.__combo_vars['strategy_window_combo_col1_var'].set('')
        self.__combo_vars['strategy_window_combo_cond_var'].set('')
        self.__entry_input_var_dict['strategy_value1'].set('')
        self.__combo_vars['strategy_window_combo_optional_col1_var'].set('')
        self.__entry_input_var_dict['strategy_value2'].set('')
        self.__combo_vars['strategy_window_combo_optional_col2_var'].set('')
        self.__combo_vars['strategy_window_combo_col2_var'].set('')
        self.__combo_vars['strategy_window_buy_sell_var'].set('')
        # Disable the value entry when no condition is selected
        self.__strategy_window_entry_value1.configure(state=tk.DISABLED)
        self.__strategy_window_entry_value2.configure(state=tk.DISABLED)
        self.__strategy_window_combo_optional_col1.configure(state=tk.DISABLED)
        self.__strategy_window_combo_optional_col2.configure(state=tk.DISABLED)
        self.__strategy_window_combo_cond1.configure(state=tk.DISABLED)
    ############################################################################################################
    def __btn_window_strategy_finalise_clicked(self):
        self.btn_strategy_window_finalise_clicked()
    ############################################################################################################
    
m = Main()
m.output_file = "strategy.py"
m.main()