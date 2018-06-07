{% extends 'NavBar.html' %}
{% block content %}
{% load static %}

    <link rel="stylesheet" media="all" type="text/css" href="{% static "library/js/jquerydatepicker/jquery-ui.css" %}"/>
    <link rel="stylesheet" media="all" type="text/css" href="{% static "library/js/jquerydatepicker/jquery-ui-timepicker-addon.css" %}"/>
    <script type="text/javascript" src="{% static "library/js/jquerydatepicker/jquery-1.10.2.min.js" %}"></script>
    <script type="text/javascript" src="{% static "library/js/jquerydatepicker/jquery-ui.min.js" %}"></script>
    <script type="text/javascript" src="{% static "library/js/jquerydatepicker/jquery-ui-timepicker-addon.js" %}"></script>
    <script type="text/javascript" src="{% static "library/js/jquerydatepicker/jquery-ui-sliderAccess.js" %}"></script>

<form action="{% url 'Class_Management:Assign_Management:GenerateAssign' %}" method="post" enctype="multipart/form-data"
              > {% csrf_token %}
<table width="100%" border="0">
  <tr>
    <td width="15%" height="577" rowspan="2" valign="top">&nbsp;</td>
    <td width="60%" rowspan="2" valign="top"><p class="assignment"><strong> Assignment</strong></p>
    <p>&nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp;
      <textarea name="Assignment" cols="80" rows="3"></textarea>
    </p>
    <p class="Detail"><strong>Assignment Detail</strong></p>
    <p>&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp; 
      <textarea name="Assignment2" cols="80" rows="5"></textarea>
    </p>
    <p class="deadline"><strong>Deadline </strong></p>
    <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <script type="text/javascript">
    $(function(){
    $("#dateInput").datetimepicker({
      dateFormat: 'yy-mm-dd',
      timeFormat: 'HH:mm:ss',
      });
});
</script>
    &nbsp;
    <input type="text" name="dateInput" id="dateInput" />
   &nbsp;&nbsp; &nbsp; </p>

    <p class="code"><strong>Code Template   </strong></p>
            <input type="file" name="upload_template" style="display:none"/>
         <input type="text"
                   name="uploadtext_template"
                   onkeydown="upload_template.value=uploadtext_template.value "
            />
            <input type="button"
                   name="uploadbutton"
                   value="Choose File"
                   onclick="upload_template.click()"
                   onmouseout="uploadtext_template.value=upload_template.value"
            />
    <p><strong>Hint</strong></p>
    <p>&nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;
      <textarea name="hint" cols="80" rows="5"></textarea>
      &nbsp;
      &nbsp;
    &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;

    </p>

        <p><strong class="testcase">Test Case</strong></p>
            <input type="file" name="upload_testcase" style="display:none"/>
         <input type="text"
                   name="uploadtext_testcase"
                    id="uploadtext_testcase"
                   onkeydown="upload_testcase.value=uploadtext_testcase.value "
                    onchange="document.getElementById('uploadtext_testcase').value = this.value.split('\\').pop().split('/').pop()"
            />
            <input type="button"
                   name="uploadbutton"
                   value="Choose File"
                   onclick="upload_testcase.click()"
                   onmouseout="uploadtext_testcase.value=upload_testcase.value"
            />
    <p>&nbsp;</p>
    <td width="25%" height="550" align="center" valign="top"><p>&nbsp;</p>  
    <button class="genquizbutton"><strong>Save</strong></button>  </tr>

  <tr>
    <td height="38" valign="top">    
  </tr>
</table>
</form>

<script>
jQuery("#jQueryUICalendar1").datepicker();
</script>
</body>
{% endblock %}  