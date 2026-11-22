
document.addEventListener("DOMContentLoaded", function () {

    console.log("IntelliFlow dashboard loaded successfully!");

    // Task form validation
    const taskForm = document.querySelector(".task-form");

    if (taskForm) {
        taskForm.addEventListener("submit", function (event) {
            const title = taskForm.querySelector(
                'input[name="title"]'
            ).value.trim();

            if (!title) {
                event.preventDefault();
                alert("Please enter a task title.");
            }
        });
    }

    // Search and filter elements
    const searchInput = document.getElementById("taskSearch");
    const statusFilter = document.getElementById("statusFilter");
    const priorityFilter = document.getElementById("priorityFilter");

    const taskItems = document.querySelectorAll(".task-item");

    function filterTasks() {
        const searchText = searchInput.value.toLowerCase().trim();
        const selectedStatus = statusFilter.value;
        const selectedPriority = priorityFilter.value;

        taskItems.forEach(function (task) {

            const title = task.dataset.title || "";
            const description = task.dataset.description || "";
            const status = task.dataset.status || "";
            const priority = task.dataset.priority || "";

            const matchesSearch =
                title.includes(searchText) ||
                description.includes(searchText);

            const matchesStatus =
                selectedStatus === "all" ||
                status === selectedStatus;

            const matchesPriority =
                selectedPriority === "all" ||
                priority === selectedPriority;

            if (matchesSearch && matchesStatus && matchesPriority) {
                task.style.display = "";
            } else {
                task.style.display = "none";
            }
        });
    }

    if (searchInput && statusFilter && priorityFilter) {
        searchInput.addEventListener("input", filterTasks);
        statusFilter.addEventListener("change", filterTasks);
        priorityFilter.addEventListener("change", filterTasks);
    }

});
