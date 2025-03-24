// txt2img and img2img tools are created as a row. With Python, we can only create
// our button before the row, not within the row. This will move the format button
// into the row.


function findTextAreaValue(parentDivId) {
    const promptDiv = document.getElementById(parentDivId);
    if (promptDiv) {
        const textArea = promptDiv.querySelector("textarea");
        if (textArea) {
            return textArea.value;
        }
    }
    return null;
}


function findInputValue(parentDivId) {
    const parentDiv = document.getElementById(parentDivId);
    if (parentDiv) {
        const inputElement = parentDiv.querySelector("input");
        if (inputElement) {
            return inputElement.value;
        }
    }
    return null;
}


async function sendPromptData() {
    const data = {
        positive_prompt: findTextAreaValue("txt2img_prompt"),
        negative_prompt: findTextAreaValue("txt2img_neg_prompt"),
        sampler: findInputValue("txt2img_sampling"),
        sampling_steps: findInputValue("txt2img_steps"),
        width: findInputValue("txt2img_width"),
        height: findInputValue("txt2img_height"),
        cfg_scale: findInputValue("txt2img_cfg_scale"),
    };

    try {
        const response = await fetch(`${window.location.origin}/save-prompt-data`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        console.log("Data saved successfully:", result);
    } catch (error) {
        console.error("Failed to save data:", error);
    }
}

function moveExtraSaveColumn() {
    let quickSettings = gradioApp().getElementById("quicksettings");
    quickSettings.appendChild(document.getElementById("cucurumba_extra_save_dir_edit"));
}

onUiLoaded(() => {
    moveExtraSaveColumn()
    const originalButton = document.getElementById("txt2img_generate");
    if (originalButton) {
        originalButton.addEventListener('click', (event) => {
            console.log("Hello Generate");
            console.log("Positive prompt: ")
            console.log(findTextAreaValue("txt2img_prompt"))
            console.log("Negative prompt: ")
            console.log(findTextAreaValue("txt2img_neg_prompt"))
            console.log("Sampler: " + findInputValue("txt2img_sampling"))
            console.log("Sampler steps: " + findInputValue("txt2img_steps"))
            console.log("Image width: " + findInputValue("txt2img_width"))
            console.log("Image height: " + findInputValue("txt2img_height"))
            console.log("CFG Scale: " + findInputValue("txt2img_cfg_scale"))
            sendPromptData().then(r => "Data saved successfully");
        });
    }
})