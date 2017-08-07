 $(document).ready(function () {
 	var modal = document.getElementById('clusterModal');
 	var btn = document.getElementByClass("cluster-btn");
 	modal.style.display = "none";
 	btn.onclick = function() {
        document.getElementByClass('cluster-link').click();
        modal.style.display = "block";
    }
 	// When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
          modal.style.display = "none";
        }
    }
        $(".xml_header").click(function () {
            $(".xml_collapse").collapse('toggle');
        });
        $(".json_header").click(function () {
            $(".json_collapse").collapse('toggle');
        });
    });