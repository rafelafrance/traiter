import numpy as np
import pandas as pd

in_name = 'vntraits110715'
out_name = in_name + '.csv'


def main():
    df = pd.read_csv(in_name)
    df.head()

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
    df.head()

    df = df.replace(np.NaN, '')
    df.head()

    df.to_csv(out_name)


if __name__ == '__main__':
    main()
