document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById("myButton");
   
    button.addEventListener('click', () => {
        updateText();
    });
});


async function updateText() {
    var text = await getPinyin("你好");
    document.getElementById("myText").innerHTML = text;
}

async function getPinyin(text) {
      const response = await fetch("/pinyin", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: text })
    });

    return await response.json();
}