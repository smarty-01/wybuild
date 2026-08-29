import type {Metadata} from "next";import "./globals.css";
export const metadata:Metadata={title:"ForgeAPK",description:"Cloud Android build platform",manifest:"/manifest.json"};
export default function Layout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}