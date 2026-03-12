<script setup lang="ts">
import { MdEditor, MdPreview } from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';

const text = ref('# Hello Editor');
</script>

<template>
  <MdEditor v-model="text" />
  <pre>{{text}}</pre>
  <MdPreview :modelValue="text" />
</template>

<style scoped>

</style>
