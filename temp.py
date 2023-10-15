import requests

url = "https://v1.nocodeapi.com/vetrof/calendar/BLDRYJNgaCLQIrfw/calendarList"
params = {}
r = requests.get(url = url, params = params)
result = r.json()
print(result)



class Course(models.Model):
    title = models.CharField(max_length=200)
    info = models.TextField(blank=True)

    def __str__(self):
        return self.title