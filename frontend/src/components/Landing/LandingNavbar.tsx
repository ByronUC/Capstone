import { Box, Container, Flex, HStack, Image, Text, Button, VStack, Link } from "@chakra-ui/react"
import { Link as RouterLink } from "@tanstack/react-router"
import { FaBars, FaCalendarCheck } from "react-icons/fa"
import { useState, useEffect } from "react"
import { Drawer } from "@/components/ui/drawer"

const navLinks = [
  { href: "#about", label: "Quiénes Somos" },
  { href: "#professionals", label: "Profesionales" },
  { href: "#why-us", label: "Por Qué Elegirnos" },
  { href: "#disorders", label: "Trastornos" },
  { href: "#prices", label: "Precios" },
  { href: "#booking", label: "Agendar" },
  { href: "#contact", label: "Contacto" },
]

export default function LandingNavbar() {
  const [isOpen, setIsOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50)
    }
    window.addEventListener("scroll", handleScroll)
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  const handleNavClick = (href: string) => {
    const element = document.querySelector(href)
    if (element) {
      element.scrollIntoView({ behavior: "smooth", block: "start" })
    }
    setIsOpen(false)
  }

  return (
    <Box
      as="header"
      position="fixed"
      top={0}
      left={0}
      width="100%"
      zIndex={1000}
      bg={scrolled ? "rgba(255, 255, 255, 0.98)" : "rgba(255, 255, 255, 0.95)"}
      backdropFilter="blur(10px)"
      boxShadow={scrolled ? "0 2px 20px rgba(45, 49, 66, 0.1)" : "0 2px 10px rgba(45, 49, 66, 0.05)"}
      transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)"
      py={scrolled ? 3 : 4}
    >
      <Container maxW="1280px">
        <Flex align="center" justify="space-between">
          {/* Logo */}
          <Flex align="center" gap={3}>
            <Image
              src="/assets/landing/logo.png"
              alt="Logo Conectemos Chile"
              width="40px"
              height="40px"
              objectFit="contain"
            />
            <Text
              fontSize="xl"
              fontWeight="bold"
              bgGradient="linear(to-r, #FFA726, #E09600)"
              bgClip="text"
              cursor="pointer"
              _hover={{ opacity: 0.8 }}
              transition="opacity 0.2s"
              onClick={() => handleNavClick("#home")}
            >
              Conectemos Chile
            </Text>
          </Flex>

          {/* Desktop Navigation */}
          <HStack
            as="nav"
            gap={6}
            display={{ base: "none", lg: "flex" }}
          >
            {navLinks.map((link) => (
              <Link
                key={link.href}
                fontSize="sm"
                fontWeight="500"
                color="gray.700"
                cursor="pointer"
                _hover={{ color: "#FFA726" }}
                transition="color 0.25s"
                onClick={() => handleNavClick(link.href)}
                whiteSpace="nowrap"
              >
                {link.label}
              </Link>
            ))}
          </HStack>

          {/* CTA Button Desktop */}
          <HStack gap={3} display={{ base: "none", lg: "flex" }} ml={8}>
            <Button
              onClick={() => handleNavClick("#booking")}
              size="md"
              bg="#E09600"
              color="black"
              fontWeight="700"
              borderRadius="full"
              px={6}
              _hover={{ bg: "#c98300", transform: "translateY(-2px)" }}
              boxShadow="0 2px 10px rgba(0, 0, 0, 0.1)"
              transition="all 0.25s"
            >
              <FaCalendarCheck style={{ marginRight: '8px' }} />
              Agendar Ahora
            </Button>
            <Button
              asChild
              size="md"
              bg="rgba(66, 133, 244, 0.2)"
              color="#1a56db"
              fontWeight="600"
              borderRadius="full"
              px={6}
              _hover={{ bg: "rgba(66, 133, 244, 0.3)" }}
              transition="all 0.25s"
            >
              <RouterLink to="/login">
                Iniciar Sesión
              </RouterLink>
            </Button>
          </HStack>

          {/* Mobile Menu Button */}
          <Button
            onClick={() => setIsOpen(true)}
            display={{ base: "flex", lg: "none" }}
            variant="ghost"
            color="gray.700"
            p={2}
          >
            <FaBars size={24} />
          </Button>
        </Flex>
      </Container>

      {/* Mobile Drawer */}
      <Drawer.Root open={isOpen} onOpenChange={(e) => setIsOpen(e.open)} placement="end">
        <Drawer.Backdrop />
        <Drawer.Content>
          <Drawer.Header>
            <Drawer.Title>Menú</Drawer.Title>
            <Drawer.CloseTrigger />
          </Drawer.Header>
          <Drawer.Body>
            <VStack align="stretch" gap={4}>
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  fontSize="lg"
                  fontWeight="500"
                  color="gray.700"
                  cursor="pointer"
                  _hover={{ color: "#FFA726" }}
                  onClick={() => handleNavClick(link.href)}
                >
                  {link.label}
                </Link>
              ))}
              <Button
                onClick={() => handleNavClick("#booking")}
                size="md"
                bg="#E09600"
                color="black"
                fontWeight="700"
                borderRadius="full"
                mt={4}
              >
                Agenda tu Hora
              </Button>
              <Button
                asChild
                size="md"
                bg="rgba(66, 133, 244, 0.2)"
                color="#1a56db"
                fontWeight="600"
                borderRadius="full"
              >
                <RouterLink to="/login">
                  Iniciar Sesión
                </RouterLink>
              </Button>
            </VStack>
          </Drawer.Body>
        </Drawer.Content>
      </Drawer.Root>
    </Box>
  )
}
