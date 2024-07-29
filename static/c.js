const imageUpload = document.getElementById("image-upload");
const selectedImage = document.getElementById("selected-image");
const removeImage = document.getElementById("remove-image");
const checkButton = document.getElementById("check-button");
const result = document.getElementById("result");

imageUpload.addEventListener("change", function (e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (event) {
            const img = new Image();
            img.src = event.target.result;

            img.onload = function () {
                const canvas = document.createElement("canvas");
                const ctx = canvas.getContext("2d");
                canvas.width = 96;
                canvas.height = 96;
                ctx.drawImage(img, 0, 0, 96, 96);
                selectedImage.src = canvas.toDataURL("image/jpeg"); // Resized image

                selectedImage.style.display = "inline";
                removeImage.style.display = "inline";
                result.textContent = ""; // Clear the result message
            };
        };
        reader.readAsDataURL(file);
    }
});

removeImage.addEventListener("click", function () {
    selectedImage.src = "";
    selectedImage.style.display = "none";
    removeImage.style.display = "none";
    imageUpload.value = "";

    result.textContent = ""; // Clear the result message
});

checkButton.addEventListener("click", function () {
    // You can handle the image upload and display the result here
    // Check if an image has been selected before submitting the form
    if (imageUpload.files.length == 0) {
        e.preventDefault(); // Prevent the form submission
        result.textContent = "Please select an image."; // Display an error message
    } else {
        result.textContent = "Checking fingerprint..."; // You may want to update this message
    }
});
