"""Utilities for working with pipes."""
import pandas as pd


def add_script(cxn, script_id, script):
    """Add a pipe to the database."""
    sql = """
        insert or replace into scripts (script_id, action) values (?, ?);"""
    cxn.execute(sql, (script_id, script))
    cxn.commit()


def select_scripts(cxn):
    """Get pipes as a dataframe."""
    sql = """select * from scripts order by script_id;"""
    return pd.read_sql(sql, cxn)
