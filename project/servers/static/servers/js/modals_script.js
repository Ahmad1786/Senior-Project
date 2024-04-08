/* Followed Modal Forms Tutorial */
/* https://blog.benoitblanchon.fr/django-htmx-modal-form/ */

//const modal = new bootstrap.Modal(document.getElementById("modal"))

htmx.on("htmx:afterSwap", (e) => {
    // Response targeting #dialog => show the modal
    if (e.detail.target.id == "dialog") { modal.show() }
})

htmx.on("htmx:beforeSwap", (e) => {
    // Empty response targeting #dialog => hide the modal
    if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
        modal.hide()
        e.detail.shouldSwap = false
    }
})

htmx.on("hidden.bs.modal", () => {
    document.getElementById("dialog").innerHTML = ""
})

// Auto reload page when new post gets added or gets edited 
// Or any other change that requires a page refresh to see new changes
document.body.addEventListener('PageRefreshNeeded', () => {
    window.location.reload();
});

function toggleJoinForm() {
    var form = document.getElementById('joinServerForm');
    form.classList.toggle('hidden');
}

function Openbar() {
    document.querySelector('.sidebar').classList.toggle('left-[-300px]')
}

function dropDown() {
    document.querySelector('#submenu').classList.toggle('hidden')
    document.querySelector('#arrow').classList.toggle('rotate-0')
}

dropDown()

function Openbar() {
    document.querySelector('.sidebar').classList.toggle('left-[-300px]')
}