<script setup>
import { ref } from 'vue'

const orgName = ref('Acme Corp')
const supportEmail = ref('support@acme.example')

const emailNotifications = ref(true)
const weeklyDigest = ref(true)
const marketingEmails = ref(false)

const saved = ref(false)
function save() {
  saved.value = true
}
</script>

<template>
  <div>
    <SHeading :level="1">Settings</SHeading>

    <SAlert v-if="saved" type="success" dismissible @dismiss="saved = false">
      Settings saved successfully.
    </SAlert>

    <SCard title="Organization">
      <SFormField label="Organization name">
        <SInput v-model="orgName" placeholder="Organization name" />
      </SFormField>
      <SFormField label="Support email" hint="Used for customer replies">
        <SInput v-model="supportEmail" placeholder="support@example.com" />
      </SFormField>
    </SCard>

    <SCard title="Notifications">
      <SSwitch v-model="emailNotifications">Email notifications</SSwitch>
      <SSwitch v-model="weeklyDigest">Weekly digest</SSwitch>
      <SSwitch v-model="marketingEmails">Marketing emails</SSwitch>
    </SCard>

    <SButton variant="primary" @click="save">Save changes</SButton>
  </div>
</template>
