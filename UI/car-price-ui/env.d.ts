//TAILDVIND SORUNU ICIN BURAYI DEGISTIRIDK TEK SATIR VARDI


/// <reference types="vite/client" />

declare module "*.vue" {
    import { DefineComponent } from "vue";
    const component: DefineComponent<{}, {}, any>;
    export default component;
}
