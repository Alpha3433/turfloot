import { Inter, DM_Sans } from 'next/font/google'
import './globals.css'
import PrivyAuthProvider from '@/components/providers/PrivyAuthProvider'
import { GameSettingsProvider } from '@/components/providers/GameSettingsProvider'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })
const dmSans = DM_Sans({ subsets: ['latin'], variable: '--font-dm-sans' })

export const metadata = {
  title: 'TurfLoot - Competitive Web3 Gaming',
  description: 'Real-time multiplayer gaming with blockchain rewards',
  metadataBase: new URL(process.env.NEXT_PUBLIC_BASE_URL || 'https://turfloot.com'),
  openGraph: {
    title: 'TurfLoot - Competitive Web3 Gaming',
    description: 'Real-time multiplayer gaming with blockchain rewards',
    url: process.env.NEXT_PUBLIC_BASE_URL || 'https://turfloot.com',
    siteName: 'TurfLoot',
    type: 'website',
  },
}

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${inter.variable} ${dmSans.variable}`}>
      <body className="min-h-screen bg-[#1E1E1E] text-white antialiased">
        <PrivyAuthProvider>
          <GameSettingsProvider>
            {children}
          </GameSettingsProvider>
        </PrivyAuthProvider>
      </body>
    </html>
  )
}