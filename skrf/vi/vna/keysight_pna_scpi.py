converters = {
    "str": str,
    "int": int,
    "float": float,
    "bool": lambda x: bool(int(x)),
}


def to_string(value):
    if type(value) in (list, tuple):
        return ",".join(map(str, value))
    elif value is None:
        return ""
    else:
        return str(value)


def scpi_preprocess(command_string, *args):
    args = list(args)
    for i, arg in enumerate(args):
        args[i] = to_string(arg)
    return command_string.format(*args)


def process_query(query, csv=False, strip_outer_quotes=True, returns="str"):
    if strip_outer_quotes is True:
        if query[0] + query[-1] in ('""', "''"):
            query = query[1:-1]
    if csv is True:
        query = query.split(",")

    converter = None if returns == "str" else converters.get(returns, None)
    if converter:
        if csv is True:
            query = list(map(converter, query))
        else:
            query = converter(query)

    return query


class SCPI(object):
    def __init__(self, resource):
        self.resource = resource

    def set_averaging_count(self, cnum=1, avg_count=""):
        scpi_command = scpi_preprocess(":SENS{:}:AVER:COUN {:}", cnum, avg_count)
        self.resource.write(scpi_command)

    def set_averaging_mode(self, cnum=1, avg_mode="SWEEP"):
        scpi_command = scpi_preprocess(":SENS{:}:AVER:MODE {:}", cnum, avg_mode)
        self.resource.write(scpi_command)

    def set_averaging_state(self, cnum=1, onoff="ON"):
        scpi_command = scpi_preprocess(":SENS{:}:AVER:STAT {:}", cnum, onoff)
        self.resource.write(scpi_command)

    def set_create_meas(self, cnum=1, mname="", param=""):
        scpi_command = scpi_preprocess(":CALC{:}:PAR:DEF:EXT '{:}','{:}'", cnum, mname, param)
        self.resource.write(scpi_command)

    def set_data(self, cnum=1, fmt="SDATA", data="None"):
        scpi_command = scpi_preprocess(":CALC{:}:DATA {:},{:}", cnum, fmt, data)
        self.resource.write(scpi_command)

    def set_delete_meas(self, cnum=1, mname=""):
        scpi_command = scpi_preprocess(":CALC{:}:PAR:DEL '{:}'", cnum, mname)
        self.resource.write(scpi_command)

    def set_display_format(self, cnum=1, fmt="MLOG"):
        scpi_command = scpi_preprocess(":CALC{:}:FORM {:}", cnum, fmt)
        self.resource.write(scpi_command)

    def set_display_trace(self, wnum="", tnum="", mname=""):
        scpi_command = scpi_preprocess(":DISP:WIND{:}:TRAC{:}:FEED '{:}'", wnum, tnum, mname)
        self.resource.write(scpi_command)

    def set_f_start(self, cnum=1, freq=""):
        scpi_command = scpi_preprocess(":SENS{:}:FREQ:START {:}", cnum, freq)
        self.resource.write(scpi_command)

    def set_f_stop(self, cnum=1, freq=""):
        scpi_command = scpi_preprocess(":SENS{:}:FREQ:STOP {:}", cnum, freq)
        self.resource.write(scpi_command)

    def set_groups_count(self, cnum=1, groups_count=1):
        scpi_command = scpi_preprocess(":SENS{:}:SWE:GRO:COUN {:}", cnum, groups_count)
        self.resource.write(scpi_command)

    def set_selected_meas(self, cnum=1, mname=""):
        scpi_command = scpi_preprocess(":CALC{:}:PAR:SEL '{:}'", cnum, mname)
        self.resource.write(scpi_command)

    def set_selected_meas_by_number(self, cnum=1, mnum=""):
        scpi_command = scpi_preprocess(":CALC{:}:PAR:MNUM {:}", cnum, mnum)
        self.resource.write(scpi_command)

    def set_sweep_mode(self, cnum=1, sweep_mode="CONT"):
        scpi_command = scpi_preprocess(":SENS{:}:SWE:MODE {:}", cnum, sweep_mode)
        self.resource.write(scpi_command)

    def set_sweep_n_points(self, cnum=1, n_points=401):
        scpi_command = scpi_preprocess(":SENS{:}:SWE:POIN {:}", cnum, n_points)
        self.resource.write(scpi_command)

    def set_sweep_type(self, cnum=1, sweep_type="LIN"):
        scpi_command = scpi_preprocess(":SENS{:}:SWE:TYPE {:}", cnum, sweep_type)
        self.resource.write(scpi_command)

    def set_trigger_source(self, trigger_source="IMM"):
        scpi_command = scpi_preprocess(":TRIG:SOUR {:}", trigger_source)
        self.resource.write(scpi_command)

    def query_active_channel(self):
        scpi_command = ":SYST:ACT:CHAN?"
        value = self.resource.query(scpi_command)
        value = process_query(value, csv=False, strip_outer_quotes=True, returns='int')
        return value

    def query_available_channels(self):
        scpi_command = ":SYST:CHAN:CAT?"
        value = self.resource.query(scpi_command)
        value = process_query(value, csv=True, strip_outer_quotes=True, returns='int')
        return value

    def query_averaging_count(self, cnum=1):
        scpi_command = scpi_preprocess(":SENS{:}:AVER:COUN?", cnum)
        value = self.resource.query(scpi_command)
        value = process_query(value, csv=False, strip_outer_quotes=True, returns='int')
        return value

    def query_averaging_mode(self, cnum=1):
        scpi_command = scpi_preprocess(":SENS{:}:AVER:MODE?", cnum)
        value = self.resource.query(scpi_command)
        value = process_query(value, csv=False, strip_outer_quotes=True, returns='str')
        return value

    def query_averaging_state(self, cnum=1):
        scpi_command = scpi_preprocess(":SENS{:}:AVER:STAT?", cnum)
        value = self.resource.query(scpi_command)
        value = process_query(value, csv=False, strip_outer_quotes=True, returns='bool')
        return value

    def query_display_format(self, cnum=1):
        scpi_command = scpi_preprocess(":CALC{:}:FORM?", cnum)
        value = self.resource.query(scpi_command)
        value = process_query(value, csv=False, strip_outer_quotes=True, returns='str')
        return value

    def query_f_start(self, cnum=1):
        scpi_command = scpi_preprocess(":SENS{:}:FREQ:START?", cnum)
        value = self.resource.query(scpi_command)
        value = process_query(value, csv=False, strip_outer_quotes=True, returns='float')
        return value

    def query_f_stop(self, cnum=1):
        scpi_command = scpi_preprocess(":SENS{:}:FREQ:STOP?", cnum)
        value = self.resource.query(scpi_command)
        value = process_query(value, csv=False, strip_outer_quotes=True, returns='float')
        return value

    def query_groups_count(self, cnum=1):
        scpi_command = scpi_preprocess(":SENS{:}:SWE:GRO:COUN?", cnum)
        value = self.resource.query(scpi_command)
        value = process_query(value, csv=False, strip_outer_quotes=True, returns='int')
        return value

    def query_meas_name_from_number(self, mnum=""):
        scpi_command = scpi_preprocess(":SYST:MEAS{:}:NAME?", mnum)
        value = self.resource.query(scpi_command)
        value = process_query(value, csv=False, strip_outer_quotes=True, returns='str')
        return value

    def query_meas_name_list(self, cnum=1):
        scpi_command = scpi_preprocess(":CALC{:}:PAR:CAT:EXT?", cnum)
        value = self.resource.query(scpi_command)
        value = process_query(value, csv=True, strip_outer_quotes=True, returns='str')
        return value

    def query_meas_number_list(self, cnum=""):
        scpi_command = scpi_preprocess(":SYST:MEAS:CAT? {:}", cnum)
        value = self.resource.query(scpi_command)
        value = process_query(value, csv=True, strip_outer_quotes=True, returns='int')
        return value

    def query_selected_meas(self, cnum=1):
        scpi_command = scpi_preprocess(":CALC{:}:PAR:SEL?", cnum)
        value = self.resource.query(scpi_command)
        value = process_query(value, csv=False, strip_outer_quotes=True, returns='str')
        return value

    def query_selected_meas_by_number(self, cnum=1):
        scpi_command = scpi_preprocess(":CALC{:}:PAR:MNUM?", cnum)
        value = self.resource.query(scpi_command)
        value = process_query(value, csv=False, strip_outer_quotes=True, returns='int')
        return value

    def query_sweep_mode(self, cnum=1):
        scpi_command = scpi_preprocess(":SENS{:}:SWE:MODE?", cnum)
        value = self.resource.query(scpi_command)
        value = process_query(value, csv=False, strip_outer_quotes=True, returns='str')
        return value

    def query_sweep_n_points(self, cnum=1):
        scpi_command = scpi_preprocess(":SENS{:}:SWE:POIN?", cnum)
        value = self.resource.query(scpi_command)
        value = process_query(value, csv=False, strip_outer_quotes=True, returns='int')
        return value

    def query_sweep_time(self, cnum=1):
        scpi_command = scpi_preprocess(":SENS{:}:SWE:TIME?", cnum)
        value = self.resource.query(scpi_command)
        value = process_query(value, csv=False, strip_outer_quotes=True, returns='float')
        return value

    def query_sweep_type(self, cnum=1):
        scpi_command = scpi_preprocess(":SENS{:}:SWE:TYPE?", cnum)
        value = self.resource.query(scpi_command)
        value = process_query(value, csv=False, strip_outer_quotes=True, returns='str')
        return value

    def query_trigger_source(self):
        scpi_command = ":TRIG:SOUR?"
        value = self.resource.query(scpi_command)
        value = process_query(value, csv=False, strip_outer_quotes=True, returns='str')
        return value

    def query_window_trace_numbers(self, wnum=""):
        scpi_command = scpi_preprocess(":DISP:WIND{:}:CAT?", wnum)
        value = self.resource.query(scpi_command)
        value = process_query(value, csv=True, strip_outer_quotes=True, returns='int')
        return value

    def query_data(self, cnum=1, fmt="SDATA"):
        scpi_command = scpi_preprocess(":CALC{:}:DATA? {:}", cnum, fmt)
        return self.resource.query_values(scpi_command)

    def query_snp_data(self, cnum=1, ports=(1, 2)):
        scpi_command = scpi_preprocess(":CALC{:}:DATA:SNP:PORT? '{:}'", cnum, ports)
        return self.resource.query_values(scpi_command)
