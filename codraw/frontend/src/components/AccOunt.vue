<template>
account

</template>


<script setup>
import { get_cookie } from '@/common';
const csrf=get_cookie('csrftoken')
console.log(csrf)

</script>
<script>
export default {
  name: 'AccOunt',
}
</script>