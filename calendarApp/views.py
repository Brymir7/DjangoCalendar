from audioop import reverse
from django.shortcuts import render
from .models import Month, Note, Day    
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
import speech_recognition as sr

def index(request):
    note_collection = Note.objects.order_by('-pub_date')
    months = Month.objects.all()
    if not Month.objects.exists():
        # Get the current month and year
        today = timezone.now()
        month_name = today.strftime("%B")
        year = today.year

        # Create a new month object
        month = Month(month_name=month_name, year=year)
        month.save()
    return render(request, 'calendarApp/index.html', {'note_collection' : note_collection, 'months': months})

class NoteCreate(CreateView):
    model = Note
    template_name = 'calendarApp/noteCreate.html'
    fields = '__all__'
    
    def form_valid(self, form):
        day = get_object_or_404(Day, pk=self.kwargs['day_id'])
        form.instance.day = day
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['day'] = get_object_or_404(Day, pk=self.kwargs['day_id'])
        return context
    
    def get_success_url(self):
        return reverse_lazy('index')
    
    
def directCreateNote(day_name, name, text):
    day = get_object_or_404(Day, day_name=day_name)
    note = Note.objects.create(note_text = text, day=day)
    
    
class NoteUpdate(UpdateView):
    model = Note
    template_name = 'calendarApp/noteCreate.html'
    fields = '__all__'
    success_url = reverse_lazy('index')


class NoteDelete(DeleteView):
    model = Note
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponse(success_url)

def speechRecognition():
    r = sr.Recognizer()

    # create a microphone instance
    mic = sr.Microphone()

    # adjust the energy threshold for ambient noise levels
    # start listening for speech
    with mic as source:
        print("Say something:")
        audio = r.listen(source)
        r.adjust_for_ambient_noise(mic)
    # recognize the speech and print the result
    try:
        text = r.recognize_google(audio)
        words = text.split(" ")
        for i in range(len(words)): #amount of words
            if words[i] == "note" or words[i] == "notes": #its a note
                words = words[i:] #splice everything before
                break
                directCreateNote() 
        #for i in range(len(words)): #iterate over the rest of the words
         #   if words[i] == "nam" or words[i] == "name" or words[i] == "title" or words[i] == "titl":
                
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Error requesting results from Google Speech Recognition service: {0}".format(e))
