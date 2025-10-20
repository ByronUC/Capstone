import { createFileRoute } from "@tanstack/react-router"
import { Box } from "@chakra-ui/react"
import LandingNavbar from "../components/Landing/LandingNavbar"
import HeroSection from "../components/Landing/HeroSection"
import AboutSection from "../components/Landing/AboutSection"
import ProfessionalsSection from "../components/Landing/ProfessionalsSection"
import WhyUsSection from "../components/Landing/WhyUsSection"
import PricesSection from "../components/Landing/PricesSection"
import DisordersSection from "../components/Landing/DisordersSection"
import TestimonialsSection from "../components/Landing/TestimonialsSection"
import BookingSection from "../components/Landing/BookingSection"
import ContactSection from "../components/Landing/ContactSection"
import LandingFooter from "../components/Landing/LandingFooter"
import FloatingButtons from "../components/Landing/FloatingButtons"

export const Route = createFileRoute("/")({
  component: LandingPage,
})

function LandingPage() {
  return (
    <Box minH="100vh">
      <LandingNavbar />
      <HeroSection />
      <AboutSection />
      <ProfessionalsSection />
      <WhyUsSection />
      <DisordersSection />
      <PricesSection />
      <TestimonialsSection />
      <BookingSection />
      <ContactSection />
      <LandingFooter />
      <FloatingButtons />
    </Box>
  )
}
