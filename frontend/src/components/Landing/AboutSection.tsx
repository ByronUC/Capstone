import { Box, Container, Heading, Text, VStack, SimpleGrid, Flex, Icon } from "@chakra-ui/react"
import { FaHeart, FaUserShield, FaCertificate, FaHandshake, FaHandHoldingHeart, FaBalanceScale } from "react-icons/fa"
import { useInView } from "react-intersection-observer"
import SpaceCarousel from "./SpaceCarousel"

export default function AboutSection() {
  const { ref, inView } = useInView({ triggerOnce: true, threshold: 0.1 })

  const values = [
    { icon: FaHeart, text: "Calidez Humana" },
    { icon: FaUserShield, text: "Confidencialidad" },
    { icon: FaCertificate, text: "Profesionalismo" },
    { icon: FaHandshake, text: "Respeto" },
    { icon: FaHandHoldingHeart, text: "Compromiso" },
    { icon: FaBalanceScale, text: "Integridad" },
  ]

  return (
    <Box
      id="about"
      py={{ base: 16, md: 24 }}
      bg="white"
      position="relative"
      ref={ref}
    >
      {/* Decorative elements */}
      <Box position="absolute" top="10%" right="5%" w="200px" h="200px" borderRadius="50%" bg="rgba(255, 167, 38, 0.05)" />

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
              Quiénes Somos
            </Heading>
            <Text fontSize={{ base: "lg", md: "xl" }} color="gray.600" maxW="800px">
              Un equipo comprometido con tu salud mental
            </Text>
          </VStack>

          <SimpleGrid columns={{ base: 1, md: 2 }} gap={12} w="full" alignItems="start">
            {/* Carousel */}
            <Box
              opacity={inView ? 1 : 0}
              transform={inView ? "translateX(0)" : "translateX(-30px)"}
              transition="all 0.8s 0.2s"
            >
              <SpaceCarousel />
            </Box>

            {/* Text content */}
            <VStack align="stretch" gap={6}>
              <Box
                bg="white"
                p={8}
                borderRadius="xl"
                boxShadow="lg"
                opacity={inView ? 1 : 0}
                transform={inView ? "translateY(0)" : "translateY(20px)"}
                transition="all 0.8s 0.3s"
              >
                <Heading as="h3" fontSize="2xl" mb={4} color="gray.800">
                  Nuestra Visión
                </Heading>
                <Text fontSize="md" color="gray.700" lineHeight="1.8">
                  Promover la importancia de la salud mental a través del acompañamiento psicológico de
                  profesionales comprometidos con cada persona de manera integral y transdisciplinaria, ofreciendo
                  una perspectiva holística y humana del quehacer profesional, creciendo en conjunto para
                  mejorar la calidad de vida de nuestros pacientes.
                </Text>
              </Box>

              <Box
                bg="white"
                p={8}
                borderRadius="xl"
                boxShadow="lg"
                opacity={inView ? 1 : 0}
                transform={inView ? "translateY(0)" : "translateY(20px)"}
                transition="all 0.8s 0.4s"
              >
                <Heading as="h3" fontSize="2xl" mb={4} color="gray.800">
                  Nuestra Misión
                </Heading>
                <Text fontSize="md" color="gray.700" lineHeight="1.8">
                  Fomentar la salud mental y emocional de personas hispanohablantes en
                  cualquier lugar del mundo, a través de la atención psicológica online. Buscamos ser parte del crecimiento
                  de cada paciente, ofreciendo herramientas emocionales y sociales que fortalezcan su bienestar y calidad
                  de vida, junto con el compromiso de apoyar también el desarrollo profesional de nuestros terapeutas.
                </Text>
              </Box>

              <Box
                bg="white"
                p={8}
                borderRadius="xl"
                boxShadow="lg"
                opacity={inView ? 1 : 0}
                transform={inView ? "translateY(0)" : "translateY(20px)"}
                transition="all 0.8s 0.5s"
              >
                <Heading as="h3" fontSize="2xl" mb={6} color="gray.800">
                  Nuestros Valores
                </Heading>
                <SimpleGrid columns={{ base: 2, md: 3 }} gap={6}>
                  {values.map((value, index) => (
                    <Flex
                      key={index}
                      direction="column"
                      align="center"
                      gap={2}
                      textAlign="center"
                    >
                      <Icon as={value.icon} fontSize="3xl" color="#4285F4" />
                      <Text fontSize="sm" fontWeight="600" color="gray.700">
                        {value.text}
                      </Text>
                    </Flex>
                  ))}
                </SimpleGrid>
              </Box>
            </VStack>
          </SimpleGrid>
        </VStack>
      </Container>
    </Box>
  )
}
