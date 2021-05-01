from django.shortcuts import render, redirect
from .forms import TopicForm
from .models import Topic
from .forms import EntryForm
from .models import Topic, Entry

# Create your views here.


def index(request):
    """the home page for learning log."""
    return render(request, "learning_logs/index.html")


def topics(request):
    topics = Topic.objects.order_by("date_added")

    context = {"topics": topics}

    return render(request, "learning_logs/topics.html", context)


def topic(request, topic_id):
    # just like we did in my_shell
    topic = Topic.objects.get(id=topic_id)
    # foreign key can be accessed using '_set'
    entries = topic.entry_set.order_by("-date_added")  # -date_added is descending order
    context = {"topic": topic, "entries": entries}

    return render(request, "learning_logs/topic.html", context)


def new_topic(request):
    if request.method != "POST":
        # no data submitted, create a blank form (create an instance of TopicForm).
        # because we included no arguments when instantiating TopicForm,
        # Django creates a blank form that the user can fill out
        form = TopicForm()
    else:
        # POST data submitted; process data
        # we make an instance of TopicForm and pass it to the data entered by the user,
        # stored in request.POST.
        form = TopicForm(data=request.POST)
        # the is_valid() method checks that all required fields have been filled
        # in (all fields in a form are required by default) and that the
        # data entered matches the field types expected
        if form.is_valid():
            # write the data from the form to the database
            form.save()
            # redirect the user's browser to the topics page
            return redirect("learning_logs:topics")

        # Display a blank form using the new_topic.html template
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)

        if form.is_valid():
            # When we call save(), we include the argument commit=False to tell Django to create
            # a new entry obejct and assign it to new_entry without saving it to the database yet

            new_entry = form.save(commit=False)
            # assign the topic of the new entry based on thetopic we pulled from topic_id
            new_entry.topic = topic
            new_entry.save()
            form.save()
            return redirect("learning_logs:topic", topic_id=topic_id)

    context = {"form": form, "topic": topic}
    return render(request, "learning_logs/new_entry.html", context)


def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != "POST":
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("MainApp:topic", topic_id=topic.id)

    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "learning_logs/edit_entry.html", context)
