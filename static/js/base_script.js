document.addEventListener("DOMContentLoaded", function() {
    console.log("The DOM is fully loaded and parsed.");
    // Your JavaScript code to run on page load
});
function makeid(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
      counter += 1;
    }
    return result;
}

function DebugAutofill(){
    document.getElementById("field_platform").value = "TEST_PLATFORM"
    document.getElementById("field_account").value = makeid(5)
    document.getElementById("field_account_type").value = "USERNAME"
    document.getElementById("field_phone").value = "+1999999"
    document.getElementById("field_password").value = makeid(12)
    document.getElementById("field_other_encrypt").value = makeid(10)
    document.getElementById("field_other_type").value = "PLACEHOLDER"
    document.getElementById("field_created_at").value = "1/1/1972 TEXT"

}
function onAddButtonClick(){
    form = document.forms["inputForm"];
    fields = document.getElementById("input-fields");
    formInfo = document.getElementById("form-action-info");

    form.action = '/add'
    form.method = 'POST'
    formInfo.innerHTML = "Fill the form to add new data.";
    fields.disabled = false;
}
function onEditButtonClick(){
    form = document.forms["inputForm"];
    fields = document.getElementById("input-fields");
    formInfo = document.getElementById("form-action-info");

    form.action = '/edit'
    form.method = 'POST'
    formInfo.innerHTML = "Use the platform and username to edit existing data.";
    fields.disabled = false;
}