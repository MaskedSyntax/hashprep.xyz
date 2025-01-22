import { Metadata } from "next"
import "./globals.css"
import { firaSans } from "./ui/fonts"

export const metadata: Metadata = {
  title: {
    template: "%s | HashPrep",
    default: "HashPrep - Interview Preparation Platform",
  },
  description: "Unlock the fun behind cracking the coding interview. Your ultimate platform for interview preparation.",
  keywords: ["interview preparation", "coding interview", "tech interview", "interview practice"],
  authors: [{ name: "Aftaab" }],
  creator: "Aftaab",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={firaSans.className}>{children}</body>
    </html>
  )
}

