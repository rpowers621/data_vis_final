pip install -U kaleido
{%for i in range(0,length)%}
    {%if titles[i]%}
    <p> {{titles[i]}} {{genre[i]}}</p>
    {%endif%}

    {% endfor %}