from optparse import OptionParser
import scrap
import database
import plot
import datetime

def separate(items):
    # gets a list of x and y and returns two lists of x and y separately. e.g:[(1, 2), (3, 4)] -> [1, 3], [2, 4]
    x = list()
    y = list()
    for item in items:
        x.append(item[0])
        y.append(item[1])
    return x, y

def utc_to_local(items):
    # gets a list of utc times and returns corresponding datetime objects. e.g -> [0, 86400] => [datetime(1970, 1, 1, 0, 0), datetime(1970, 1, 2, 0, 0)]
    locals = list()
    for item in items:
        locals.append(datetime.datetime.utcfromtimestamp(item))
    return locals

def get_options():
    parser = OptionParser()
    parser.add_option('-t', '--time', help='time to wait for JS to load webpage', default=5, dest='wait')
    parser.add_option('-n', '--dbfilename', help='name of the database file', default='data.sqlite3', dest='dbfilename')
    parser.add_option('-p', '--path', help='path to chrome driver', default='/usr/local/bin/chromedriver', dest='path')
    parser.add_option('-s', '--scatter', help='scatter the given input', default='', dest='scatter')
    parser.add_option('-u', '--update', help='whether updates its database or no', default=False, action='store_true', dest='update')
    parser.add_option('-r', '--rotation', help='rotation of dates in figure', default=30, dest='rotation')
    return parser.parse_args()[0]

args = get_options()
if args.update:
    db = scrap.scrap(args.dbfilename, args.wait, args.path)
else:
    db = database.DB(args.dbfilename)

if args.scatter:
    material = args.scatter
    data = db.get_all_material_data(material)
    x, y = separate(data)
    x = utc_to_local(x)
    plot.plot_date(x, y, 'Dates', 'Prices', args.rotation)
    


