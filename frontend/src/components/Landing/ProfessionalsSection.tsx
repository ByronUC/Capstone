import { Box, Container, Heading, Text, VStack, SimpleGrid, Image, Button, Flex, Badge } from "@chakra-ui/react"
import { FaCalendarCheck, FaEnvelope } from "react-icons/fa"
import { useInView } from "react-intersection-observer"

export default function ProfessionalsSection() {
  const { ref, inView } = useInView({ triggerOnce: true, threshold: 0.1 })

  const handleNavClick = (href: string) => {
    const element = document.querySelector(href)
    if (element) {
      element.scrollIntoView({ behavior: "smooth", block: "start" })
    }
  }

  const professionals = [
    {
      name: "Ángel Díaz",
      title: "Director, Psicólogo Clínico y Máster en Terapias de Parejas",
      image: "/assets/landing/terapista_angel.webp",
      description: "Psicólogo clínico con más de 8 años de experiencia con enfoque en psicoanálisis, especializado en terapia individual y de pareja, sexología y violencia en la relación. Integra herramientas de coaching deportivo y test proyectivos (OQ 42.2, TRO, HTP, Test del Árbol, Persona bajo la lluvia y Test de la Familia) para profundizar en el proceso terapéutico.",
      specialties: ["Depresión / Ansiedad", "Terapia de Pareja", "Inseguridad / Autoestima", "Terapia Psicoanalítica"],
      action: { type: "booking", label: "Agendar con Ángel" }
    },
    {
      name: "Juan Pablo Schiaffino",
      title: "Gerente del Área de Marketing y Telecomunicaciones",
      image: "/assets/landing/gerente_pp.webp",
      description: "Profesional con experiencia en gestión estratégica de comunicación digital, marketing y desarrollo tecnológico. Su enfoque combina innovación, análisis de datos y visión creativa para fortalecer la presencia digital de Conectemos Chile, potenciando el vínculo entre la psicología y la tecnología aplicada al bienestar humano.",
      specialties: ["Marketing Digital", "Telecomunicaciones", "Estrategia y Branding", "Gestión de Proyectos"],
      action: { type: "link", label: "Contactar a Juan Pablo", url: "https://www.wisestlabs.cl" }
    }
  ]

  return (
    <Box
      id="professionals"
      py={{ base: 16, md: 24 }}
      bg="gray.50"
      position="relative"
      ref={ref}
    >
      {/* Decorative elements */}
      <Box position="absolute" top="10%" left="5%" w="200px" h="200px" borderRadius="50%" bg="rgba(66, 133, 244, 0.05)" />

      <Container maxW="1280px">
        <VStack gap={12}>
          <VStack
            gap={4}
            textAlign="center"
            opacity={inView ? 1 : 0}
            transform={inView ? "translateY(0)" : "translateY(30px)"}
            transition="all 0.6s"
          >
            <Heading
              as="h2"
              fontSize={{ base: "3xl", md: "4xl", lg: "5xl" }}
              fontWeight="700"
              color="gray.800"
            >
              Nuestros Profesionales
            </Heading>
            <Text fontSize={{ base: "lg", md: "xl" }} color="gray.600" maxW="800px">
              Especialistas comprometidos con tu bienestar
            </Text>
          </VStack>

          <SimpleGrid columns={{ base: 1, lg: 2 }} gap={8} w="full">
            {professionals.map((professional, index) => (
              <Box
                key={index}
                bg="white"
                borderRadius="2xl"
                overflow="hidden"
                boxShadow="xl"
                opacity={inView ? 1 : 0}
                transform={inView ? "translateY(0)" : "translateY(30px)"}
                transition={`all 0.8s ${0.2 + index * 0.1}s`}
                _hover={{ transform: "translateY(-8px)", boxShadow: "2xl" }}
              >
                <Image
                  src={professional.image}
                  alt={professional.name}
                  w="full"
                  h={{ base: "300px", md: "400px" }}
                  objectFit="cover"
                />

                <VStack align="stretch" p={8} gap={4}>
                  <Heading as="h3" fontSize="2xl" color="gray.800">
                    {professional.name}
                  </Heading>
                  <Text fontSize="md" fontWeight="600" color="#4285F4">
                    {professional.title}
                  </Text>

                  <Text fontSize="md" color="gray.700" lineHeight="1.8">
                    {professional.description}
                  </Text>

                  <Flex flexWrap="wrap" gap={2} mt={2}>
                    {professional.specialties.map((specialty, idx) => (
                      <Badge
                        key={idx}
                        colorScheme="blue"
                        px={3}
                        py={1}
                        borderRadius="full"
                        fontSize="xs"
                      >
                        {specialty}
                      </Badge>
                    ))}
                  </Flex>

                  {professional.action.type === "booking" ? (
                    <Button
                      mt={4}
                      bg="#E09600"
                      color="black"
                      fontWeight="700"
                      borderRadius="full"
                      leftIcon={<FaCalendarCheck />}
                      _hover={{ bg: "#c98300" }}
                      onClick={() => handleNavClick("#booking")}
                    >
                      {professional.action.label}
                    </Button>
                  ) : (
                    <Button
                      as="a"
                      href={professional.action.url}
                      target="_blank"
                      rel="noopener"
                      mt={4}
                      bg="#4285F4"
                      color="white"
                      fontWeight="700"
                      borderRadius="full"
                      leftIcon={<FaEnvelope />}
                      _hover={{ bg: "#3264C8" }}
                    >
                      {professional.action.label}
                    </Button>
                  )}
                </VStack>
              </Box>
            ))}
          </SimpleGrid>
        </VStack>
      </Container>
    </Box>
  )
}
