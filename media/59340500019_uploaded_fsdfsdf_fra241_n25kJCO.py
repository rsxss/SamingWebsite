{% extends "NavBar.html" %}
{% block content %}
{% load static %}
<body background="{% static '/grading_code/images/background.png' %}">
<table width="100%" border="0">
  <tr>
      <center><H1><u>{{ classname }}</u></H1></center>
    <td height="137" colspan="4" valign="top"><p>&nbsp;</p>
      <p><center> <img src="{% static "png/person.png" %}" width="90" height="90">&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; <img src="{% static "png/person.png" %}" width="90" height="90"></center></p>      </td>
    </tr>
  <tr>
    <td width="15%" height="67" valign="top">&nbsp;</td>
    <td width="12%" valign="top">    
    <td width="28%" valign="top"><p class="teacher1"><span class="teacher1"><span class="teacher1"><strong>Teacher : Admin 1</strong></span></span></p>
    <p class="teacher1"><span class="teacher1"><span class="teacher1"><strong>Email : admin1@mail.kmutt.ac.th </strong></span></span></p>            
    <td width="45%" valign="top"><p class="teacher2"><strong><span class="teacher2">Teacher : Admin 2</span></strong></p>
    <p class="teacher2"><strong><span class="teacher2">Email : admin2@mail.kmutt.ac.th </span></strong></p>        
  </tr>
</table>
{%  for i in quiz %}
  <tr>
          <script>console.log(i)</script>
    <td height="465" colspan="4" valign="top"><center>
        <p><a href={% url 'Class_Management:Assign_Management:Uploadfile' i.id %} class="button" >
          <strong>Assignment : {{ i.quizTitle }}<br>
          Detail : {{ i.quizDetail }} <br>
          Deadline : {{ i.deadline }} <br>
        </strong></a>    </p>
    </center>
    </td>
      {%  if request.user.is_superuser %}
  <td height="465" colspan="4" valign="top">
      <form action="{% url 'Class_Management:Assign_Management:DeleteAssign' i.id %}" method="post" style="display: inline;">
          {% csrf_token %}
          <input type="hidden" name="quiz_id" value="{{ i.id }}" />
          <center><button type="submit" class="genquizbutton">
              <span class="glyphicon glyphicon-remove"></span>Delete
          </button></center>
      </form>
  </td>
  {% endif %}
  </tr>
    {% endfor %}

<script>
jQuery("#jQueryUICalendar1").datepicker();
</script>
</body>
{% endblock content %}