import { Box, Container, Heading, Text, Button, HStack, VStack, Flex, Icon } from "@chakra-ui/react"
import { FaCalendarAlt, FaInfoCircle, FaCertificate, FaClock, FaFileInvoiceDollar } from "react-icons/fa"
import { useInView } from "react-intersection-observer"

export default function HeroSection() {
  const { ref, inView } = useInView({ triggerOnce: true, threshold: 0.1 })

  const handleNavClick = (e: React.MouseEvent<HTMLAnchorElement>, href: string) => {
    e.preventDefault()
    const element = document.querySelector(href)
    if (element) {
      element.scrollIntoView({ behavior: "smooth", block: "start" })
    }
  }

  return (
    <Box
      id="home"
      position="relative"
      minH="100vh"
      display="flex"
      alignItems="center"
      bgImage="url('/assets/landing/hero-section.webp')"
      bgSize="cover"
      bgPosition="center"
      bgAttachment={{ base: "scroll", md: "fixed" }}
      _before={{
        content: '""',
        position: "absolute",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        bg: "rgba(45, 49, 66, 0.75)",
        zIndex: 1,
      }}
      ref={ref}
    >
      {/* Decorative shapes */}
      <Box position="absolute" top="20%" left="10%" w="300px" h="300px" borderRadius="full" bg="rgba(255, 167, 38, 0.1)" filter="blur(100px)" zIndex={1} />
      <Box position="absolute" bottom="20%" right="10%" w="400px" h="400px" borderRadius="full" bg="rgba(66, 133, 244, 0.1)" filter="blur(120px)" zIndex={1} />

      <Container maxW="1280px" position="relative" zIndex={2} py={{ base: "120px", md: "80px" }}>
        <VStack
          gap={8}
          align="center"
          textAlign="center"
          opacity={inView ? 1 : 0}
          transform={inView ? "translateY(0)" : "translateY(30px)"}
          transition="all 0.8s cubic-bezier(0.215, 0.61, 0.355, 1)"
        >
          <Heading
            as="h1"
            fontSize={{ base: "3xl", md: "5xl", lg: "6xl" }}
            fontWeight="800"
            color="white"
            maxW="900px"
            lineHeight="1.2"
          >
            Tu bienestar emocional es nuestra prioridad
          </Heading>

          <Text
            fontSize={{ base: "lg", md: "xl" }}
            color="whiteAlpha.900"
            maxW="700px"
            lineHeight="1.8"
          >
            En Conectemos Chile contamos con profesionales especializados para acompañarte en tu proceso terapéutico y ayudarte a encontrar el equilibrio que buscas.
          </Text>

          <HStack gap={4} flexWrap="wrap" justify="center">
            <Button
              as="a"
              href="#booking"
              size="lg"
              bg="#E09600"
              color="black"
              fontWeight="700"
              borderRadius="full"
              px={8}
              py={6}
              leftIcon={<FaCalendarAlt />}
              _hover={{ bg: "#c98300", transform: "translateY(-2px)" }}
              boxShadow="0 4px 20px rgba(224, 150, 0, 0.4)"
              transition="all 0.25s"
              onClick={(e) => handleNavClick(e, "#booking")}
            >
              Agenda tu primera sesión
            </Button>
            <Button
              as="a"
              href="#disorders"
              size="lg"
              bg="rgba(66, 133, 244, 0.2)"
              color="white"
              fontWeight="600"
              borderRadius="full"
              px={8}
              py={6}
              leftIcon={<FaInfoCircle />}
              _hover={{ bg: "rgba(66, 133, 244, 0.3)" }}
              transition="all 0.25s"
              onClick={(e) => handleNavClick(e, "#disorders")}
            >
              Conoce más
            </Button>
          </HStack>

          <Flex
            gap={{ base: 4, md: 8 }}
            mt={8}
            flexWrap="wrap"
            justify="center"
          >
            {[
              { icon: FaCertificate, text: "Profesionales certificados" },
              { icon: FaClock, text: "Molidad online/presencial" },
              { icon: FaFileInvoiceDollar, text: "Boletas reembolsables" },
            ].map((feature, index) => (
              <Flex
                key={index}
                align="center"
                gap={2}
                bg="whiteAlpha.200"
                backdropFilter="blur(10px)"
                px={4}
                py={3}
                borderRadius="full"
                opacity={inView ? 1 : 0}
                transform={inView ? "translateY(0)" : "translateY(20px)"}
                transition={`all 0.6s cubic-bezier(0.215, 0.61, 0.355, 1) ${0.3 + index * 0.1}s`}
              >
                <Icon as={feature.icon} color="#FFA726" fontSize="xl" />
                <Text color="white" fontSize="sm" fontWeight="500">
                  {feature.text}
                </Text>
              </Flex>
            ))}
          </Flex>
        </VStack>
      </Container>
    </Box>
  )
}
