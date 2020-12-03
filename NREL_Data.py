import pandas as pd

full_data = pd.read_csv('data/zip_codes_states.csv')
ca_data = full_data[full_data['state'] == 'CA'].reset_index()

auth_file = open('data/auth.txt', 'r')
auth_dict = {}
for line in auth_file:
    auth_dict[line.strip().split()[0]] = line.strip().split()[1]

# This code taken from NREL's NRDSB API site
# Declare all variables as strings. Spaces must be replaced with '+', i.e., change 'John Smith' to 'John+Smith'.
# You must request an NSRDB api key from the link above
api_key = auth_dict['api']
# Set the attributes to extract (e.g., dhi, ghi, etc.), separated by commas.
attributes = 'ghi'
# Choose year of data
year = 2015
# Set leap year to true or false. True will return leap day data if present, false will not.
leap_year = 'false'
# Set time interval in minutes, i.e., '30' is half hour intervals. Valid intervals are 30 & 60.
interval = '60'
# Specify Coordinated Universal Time (UTC), 'true' will use UTC, 'false' will use the local time zone of the data.
# NOTE: In order to use the NSRDB data in SAM, you must specify UTC as 'false'. SAM requires the data to be in the
# local time zone.
utc = 'false'
# Your full name, use '+' instead of spaces.
your_name = auth_dict['name']
# Your reason for using the NSRDB.
reason_for_use = 'academic+research'
# Your affiliation
your_affiliation = 'Purdue+University'
# Your email address
your_email = auth_dict['email']
# Please join our mailing list so we can keep you up-to-date on new developments.
mailing_list = 'false'

ghi_dict = {}
start_index = 205
lim = 208

for index, row in ca_data.iloc[start_index:lim].iterrows():
    lat, lon = row['latitude'], row['longitude']
    df = pd.read_csv('http://developer.nrel.gov/api/solar/nsrdb_0512_download.csv?wkt=POINT({lon}%20{lat})'
                 '&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}'
                 '&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}'
                 '&attributes={attr}'.format(year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc,
                                             name=your_name, email=your_email, mailing_list=mailing_list,
                                             affiliation=your_affiliation, reason=reason_for_use, api=api_key,
                                             attr=attributes), skiprows=2)

    # Set the time index in the pandas dataframe:
    df = df.set_index(pd.date_range('1/1/{yr}'.format(yr=year), freq=interval+'Min', periods=525600/int(interval)))
    mean_ghi = df['GHI'].mean()
    ghi_dict[row['zip_code']] = mean_ghi

# take a look
ghi_data = pd.DataFrame.from_dict(ghi_dict, orient='index', columns=['GHI'])
ghi_data.to_csv('ghi_data_'+str(start_index)+'_'+str(lim)+'.csv')

