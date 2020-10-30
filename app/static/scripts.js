function key_log(key, imageData) {
    const form = new FormData()
    form.append('key', key)
    form.append('width', imageData.width)
    form.append('height', imageData.height)
    form.append(
        'frame', 
        new Blob([imageData.data.buffer], { type: 'image/jpeg' }), 
        `frame_before_${key}.jpg`
    )

    return fetch('/frame_key_log', { 
        method: 'POST',
        body: form
    })
    .then(resp => resp.json())
    .then(data => console.log(data))
}

function getImageData(img, canvas) {
    const width = img.clientWidth
    const height = img.clientHeight
    const context = canvas.getContext('2d')
    context.drawImage(img, 0, 0)
    return context.getImageData(0, 0, width, height)
}

window.addEventListener('DOMContentLoaded', () => {
    const img = document.getElementById('image')
    const canvas = document.getElementById('canvas')

    document.addEventListener('keydown', event => {
        const { keyCode } = event
        const imageData = getImageData(img, canvas)
        key_log(keyCode, imageData)
    })
})