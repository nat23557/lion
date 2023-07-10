{% if user.is_authenticated %}
      <h3>Add a Comment:</h3>
      <form method="post">
          {% csrf_token %}
          {{ form.as_p }}
          <button type="submit">Add Comment</button>
      </form>
  {% else %}
      <p>Please <a href="{% url 'login' %}">login</a> to add a comment.</p>
  {% endif %}