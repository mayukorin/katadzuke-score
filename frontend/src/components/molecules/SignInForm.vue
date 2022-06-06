<template>
  <v-form ref="form">
    <v-text-field
      v-model="form.email"
      label="メールアドレス"
      :rules="rules.email"
      prepend-icon="mdi-email"
    />
    <v-spacer></v-spacer>
    <v-text-field
      v-model="form.password"
      label="パスワード"
      :rules="rules.password"
      prepend-icon="mdi-lock"
    />
    <ContainedButton @click="handleClick" :is-loading="isLoading"
      >ログイン</ContainedButton
    >
  </v-form>
</template>

<script>
import ContainedButton from "@/components/atoms/ContainedButton";
// メールアドレスのフォーマット
const REGEX_EMAIL = /.+@.+/;

export default {
  name: "SignInForm",
  components: {
    ContainedButton,
  },
  props: {
    isLoading: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      form: {
        email: "",
        password: "",
      },
      rules: {
        email: [
          (v) => !!v || "メールアドレスを入力してください",
          (v) => REGEX_EMAIL.test(v) || "メールアドレスの形式が間違っています",
        ],
        password: [(v) => !!v || "パスワードを入力してください"],
      },
    };
  },
  methods: {
    handleClick() {
      //console.log(ev);
      if (!this.$refs.form.validate()) return;
      // ok と出力されるはず
      this.$emit("signin-button-click", {
        email: this.form.email,
        password: this.form.password,
      });
      /*
        this.onlogin({ email: this.form.email, password: this.form.password})
            .catch(err => {
                console.log(err);
            })
            .then(() => {
                console.log('ログイン完了')
            })
        */
    },
  },
};
</script>
