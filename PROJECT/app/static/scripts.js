<script>
  var ctx = document.getElementById('skillsChart').getContext('2d');
  var labels = {{ resume_data.top_skillset.keys() | list | tojson }};
  var data = {{ resume_data.top_skillset.values() | list | tojson }};

  var skillsChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Skill Proficiency',
        data: data,
        // you can still hard-code colors or generate them dynamically if you like:
        backgroundColor: ['#1abc9c', '#3498db', '#9b59b6', '#e74c3c', '#f39c12']
      }]
    },
    options: {
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
</script>
