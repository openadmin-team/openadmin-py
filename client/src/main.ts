// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { createApp } from "vue"
import { VueQueryPlugin } from "@tanstack/vue-query"
import "./style.css"
import App from "./App.vue"
import { router } from "./router"

createApp(App).use(router).use(VueQueryPlugin).mount("#app")
