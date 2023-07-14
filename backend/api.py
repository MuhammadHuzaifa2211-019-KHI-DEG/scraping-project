
# # from flask import Flask, jsonify
# # from apscheduler.schedulers.background import BackgroundScheduler
# # from script import scrape_jobs

# # app = Flask(__name__)

# # scheduler = BackgroundScheduler()

# # def run_scraper():
# #     scraped_data = scrape_jobs()
# #     # Do something with the scraped data (e.g., save to database, send notifications, etc.)

# # @app.route('/jobs', methods=['GET'])
# # def jobs():
# #     return scrape_jobs()

# # if __name__ == '__main__':
# #     # Schedule the job to run every 10 minutes for three days
# #     scheduler.add_job(run_scraper, 'interval', minutes=10, end_date='2023-07-16')
# #     scheduler.start()

# #     app.run(port=5003)



from flask import Flask, jsonify
from script import scrape_jobs
from apscheduler.schedulers.background import BackgroundScheduler
import csv
import json
# import datetime
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/', methods=['GET'])
def jobs():
    try:
        filename = 'job_data.csv'
        job_data = read_csv_file(filename)

        current_date = datetime.now().strftime("%Y-%m-%d")
        data = {
        "date": current_date,
        "job_data": job_data
    }
        return jsonify(data)
        # return jsonify({"job_data": job_data})
    
    except Exception as e:
        print(e)
        return jsonify({"error":"No data found"})

def read_csv_file(filename):
    job_data = []
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            job_data.append(row)
    return job_data

scheduler = BackgroundScheduler()
scheduler.add_job(scrape_jobs, 'cron', minute='*', next_run_time=datetime.now())
scheduler.start()
 
if __name__ == '__main__':
    app.run(port=5000,host='0.0.0.0')
