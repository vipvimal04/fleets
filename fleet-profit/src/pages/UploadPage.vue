<template>

<q-page padding>

<q-file
v-model="file"
label="Upload Fleet Excel"
/>

<q-btn
label="Upload"
color="primary"
class="q-mt-md"
@click="uploadFile"
/>

</q-page>

</template>

<script>

import axios from "axios"

export default {

data(){

return {

file:null

}

},

methods:{

async uploadFile(){

let formData = new FormData()

formData.append("file",this.file)

await axios.post(
"http://localhost:5000/upload",
formData
)

this.$q.notify("Upload successful")

}

}

}

</script>