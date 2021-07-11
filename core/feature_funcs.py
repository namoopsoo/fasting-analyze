

def evening_hours(data):
    return all([18 <= x <=23 for x in data])


def feat_LastTwoFastsStartedBeforeMidnight(df):
    return df['StartHour'].shift(-1).rolling(2).apply(evening_hours)


def feat_RollingHoursMean2Fasts(df):
    return df['Hours'].shift(-1).rolling(2).mean()


