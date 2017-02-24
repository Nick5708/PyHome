import bottle
import time
import sqlite3

conn = sqlite3.connect('/tmp/database.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS CO2 (UTime INT, Data INT)')

@bottle.route('/exit')
def powerOff():
	conn.close()
	exit(0)

@bottle.route('/co<data>')
def handler(data1,data2,data3):
	print(data1,data2,data3)
	c.execute("INSERT INTO CO2 VALUES (" + str(time.time() * 1000) +",  "+  data +")")
	conn.commit()
	return 'OK'

@bottle.route('/')
def test():
	html = '''
     <!doctype html>
 <html>
  <head>
    <script type='text/javascript' src='https://www.gstatic.com/charts/loader.js'></script>
    <script type='text/javascript'>
      google.charts.load('current', {'packages':['line']});
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('date', 'Время');
        data.addColumn('number', 'Уровень CO2');
        data.addRows([  \r\n'''
	for row in c.execute('SELECT * FROM CO2 ORDER BY UTime'):
			print(row[0])
			if (row[0] > (time.time()*1000 - 86400)):
				html += ' [new Date( ' + str(row[0]) + ' ), ' + str(row[1]) + ' ], \r\n '
	html += ''']);
        var options = {'title':'График температур',
        'width':1000,
        'height':500 };
         var chart = new google.charts.Line(document.getElementById('linechart_material'));
        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id='linechart_material'></div>
  </body>
</html>

 '''
	return html

bottle.run(host='0.0.0.0', port=80, debug=True)
