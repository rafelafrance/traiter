import numpy as np
import pandas as pd

# File names
in_name = 'vntraits110715'
out_name = in_name + '.csv'


def main():
    df = pd.read_csv(in_name)
    # df.head()

    # Add columns that we will fill in later
    # Note: Pandas adds a row number column at column #0
    df['dwc_sex'] = None
    df['dwc_sex_source'] = None
    df['dwc_lifeStage'] = None
    df['dwc_lifeStage_source'] = None
    df['vto_bodyLength'] = None
    df['vto_bodyLength_units'] = None
    df['vto_bodyLength_source'] = None
    df['vto_bodyMass'] = None
    df['vto_bodyMass_units'] = None
    df['vto_bodyMass_source'] = None
    # df.head()

    # Remove NaNs added by PAndas
    df = df.replace(np.NaN, '')
    # df.head()

    # Output new CSV file
    df.to_csv(out_name)


if __name__ == '__main__':
    main()
