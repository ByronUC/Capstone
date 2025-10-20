import { Box, Container, Flex, Text, VStack, HStack, Link, Icon, Image, SimpleGrid } from "@chakra-ui/react"
import { FaInstagram, FaTiktok, FaWhatsapp, FaEnvelope, FaPhone, FaMapMarkerAlt, FaClock } from "react-icons/fa"

export default function LandingFooter() {
  const currentYear = new Date().getFullYear()

  const handleNavClick = (e: React.MouseEvent<HTMLAnchorElement>, href: string) => {
    e.preventDefault()
    const element = document.querySelector(href)
    if (element) {
      element.scrollIntoView({ behavior: "smooth", block: "start" })
    }
  }

  return (
    <Box as="footer" bg="#2D3142" color="white" position="relative" overflow="hidden">
      {/* Wave decoration */}
      <Box position="absolute" top={0} left={0} right={0} h="100px" opacity={0.05}>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" preserveAspectRatio="none" style={{ width: '100%', height: '100%' }}>
          <path fill="#4285F4" fillOpacity="1" d="M0,192L48,208C96,224,192,256,288,261.3C384,267,480,245,576,218.7C672,192,768,160,864,165.3C960,171,1056,213,1152,224C1248,235,1344,213,1392,202.7L1440,192L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
        </svg>
      </Box>

      <Container maxW="1280px" py={16} position="relative" zIndex={1}>
        <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} gap={12} mb={12}>
          {/* Logo and description */}
          <VStack align="start" gap={4}>
            <Flex align="center" gap={3}>
              <Image
                src="/assets/landing/logo.png"
                alt="Logo Conectemos Chile"
                width="40px"
                height="40px"
                objectFit="contain"
              />
              <Text fontSize="xl" fontWeight="bold" color="white">
                Conectemos Chile
              </Text>
            </Flex>
            <Text fontSize="sm" color="gray.300" lineHeight="1.8">
              En Conectemos Chile estamos comprometidos con tu bienestar emocional y psicológico. Nuestro equipo de profesionales está aquí para acompañarte en tu proceso de crecimiento personal.
            </Text>
          </VStack>

          {/* Quick links */}
          <VStack align="start" gap={3}>
            <Text fontSize="lg" fontWeight="700" mb={2} color="white">
              Enlaces Rápidos
            </Text>
            <Link href="#home" fontSize="sm" color="gray.300" _hover={{ color: "#FFA726" }} transition="color 0.2s" onClick={(e) => handleNavClick(e, "#home")}>
              Inicio
            </Link>
            <Link href="#about" fontSize="sm" color="gray.300" _hover={{ color: "#FFA726" }} transition="color 0.2s" onClick={(e) => handleNavClick(e, "#about")}>
              Quiénes Somos
            </Link>
            <Link href="#professionals" fontSize="sm" color="gray.300" _hover={{ color: "#FFA726" }} transition="color 0.2s" onClick={(e) => handleNavClick(e, "#professionals")}>
              Nuestros Profesionales
            </Link>
            <Link href="#why-us" fontSize="sm" color="gray.300" _hover={{ color: "#FFA726" }} transition="color 0.2s" onClick={(e) => handleNavClick(e, "#why-us")}>
              Por Qué Elegirnos
            </Link>
            <Link href="#disorders" fontSize="sm" color="gray.300" _hover={{ color: "#FFA726" }} transition="color 0.2s" onClick={(e) => handleNavClick(e, "#disorders")}>
              Trastornos que Tratamos
            </Link>
            <Link href="#prices" fontSize="sm" color="gray.300" _hover={{ color: "#FFA726" }} transition="color 0.2s" onClick={(e) => handleNavClick(e, "#prices")}>
              Precios
            </Link>
            <Link href="#testimonials" fontSize="sm" color="gray.300" _hover={{ color: "#FFA726" }} transition="color 0.2s" onClick={(e) => handleNavClick(e, "#testimonials")}>
              Testimonios
            </Link>
            <Link href="#booking" fontSize="sm" color="gray.300" _hover={{ color: "#FFA726" }} transition="color 0.2s" onClick={(e) => handleNavClick(e, "#booking")}>
              Agendar
            </Link>
            <Link href="#contact" fontSize="sm" color="gray.300" _hover={{ color: "#FFA726" }} transition="color 0.2s" onClick={(e) => handleNavClick(e, "#contact")}>
              Contacto
            </Link>
          </VStack>

          {/* Contact info */}
          <VStack align="start" gap={4}>
            <Text fontSize="lg" fontWeight="700" mb={2} color="white">
              Contáctanos
            </Text>
            <HStack align="start" gap={3}>
              <Icon as={FaMapMarkerAlt} color="#FFA726" fontSize="lg" mt={1} />
              <Text fontSize="sm" color="gray.300">
                Adolfo Bombero Ossa 1010, Oficina 204, Santiago
              </Text>
            </HStack>
            <HStack gap={3}>
              <Icon as={FaPhone} color="#FFA726" fontSize="lg" />
              <Link href="tel:+56921991963" fontSize="sm" color="gray.300" _hover={{ color: "#FFA726" }}>
                +56 9 2199 1963
              </Link>
            </HStack>
            <HStack gap={3}>
              <Icon as={FaEnvelope} color="#FFA726" fontSize="lg" />
              <Link href="mailto:conectemoscl@gmail.com" fontSize="sm" color="gray.300" _hover={{ color: "#FFA726" }}>
                conectemoscl@gmail.com
              </Link>
            </HStack>
            <HStack align="start" gap={3}>
              <Icon as={FaClock} color="#FFA726" fontSize="lg" mt={1} />
              <VStack align="start" gap={0}>
                <Text fontSize="sm" color="gray.300">Lun-Vie: 9:00 - 20:00</Text>
                <Text fontSize="sm" color="gray.300">Sáb: 9:00 - 19:00</Text>
                <Text fontSize="sm" color="gray.300">Dom: 9:00 - 14:00</Text>
              </VStack>
            </HStack>
          </VStack>

          {/* Social media */}
          <VStack align="start" gap={4}>
            <Text fontSize="lg" fontWeight="700" mb={2} color="white">
              Síguenos
            </Text>
            <HStack gap={4}>
              <Link
                href="https://www.instagram.com/conectemos.chile?igsh=MXNseDRxZGYyZGxwcA=="
                target="_blank"
                rel="noopener noreferrer"
              >
                <Box
                  bg="rgba(255, 167, 38, 0.1)"
                  p={3}
                  borderRadius="lg"
                  _hover={{ bg: "rgba(255, 167, 38, 0.2)", transform: "translateY(-3px)" }}
                  transition="all 0.2s"
                >
                  <Icon as={FaInstagram} fontSize="2xl" color="#FFA726" />
                </Box>
              </Link>
              <Link
                href="https://www.tiktok.com/@psicologo.ngel.da?_t=ZM-8zSsKIxiNRG&_r=1"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Box
                  bg="rgba(255, 167, 38, 0.1)"
                  p={3}
                  borderRadius="lg"
                  _hover={{ bg: "rgba(255, 167, 38, 0.2)", transform: "translateY(-3px)" }}
                  transition="all 0.2s"
                >
                  <Icon as={FaTiktok} fontSize="2xl" color="#FFA726" />
                </Box>
              </Link>
              <Link
                href="https://wa.me/56921991963?text=Hola,%20me%20gustaría%20agendar%20una%20consulta%20en%20Conectemos%20Chile"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Box
                  bg="rgba(255, 167, 38, 0.1)"
                  p={3}
                  borderRadius="lg"
                  _hover={{ bg: "rgba(255, 167, 38, 0.2)", transform: "translateY(-3px)" }}
                  transition="all 0.2s"
                >
                  <Icon as={FaWhatsapp} fontSize="2xl" color="#FFA726" />
                </Box>
              </Link>
            </HStack>
          </VStack>
        </SimpleGrid>

        {/* Bottom bar */}
        <Box pt={8} mt={8} borderTop="1px solid" borderColor="rgba(255, 255, 255, 0.1)">
          <Flex
            direction={{ base: "column", md: "row" }}
            justify="center"
            align="center"
            gap={4}
          >
            <Text fontSize="sm" color="gray.400" textAlign="center">
              © {currentYear} Conectemos Chile. Todos los derechos reservados.
            </Text>
          </Flex>
        </Box>
      </Container>
    </Box>
  )
}
