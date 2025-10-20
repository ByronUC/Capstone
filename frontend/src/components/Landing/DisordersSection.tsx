import { Box, Container, Heading, Text, VStack, SimpleGrid, Icon } from "@chakra-ui/react"
import { FaBrain, FaCloudRain, FaUsers, FaMoon, FaHeart, FaBriefcase, FaHandHoldingHeart, FaPuzzlePiece } from "react-icons/fa"
import { useInView } from "react-intersection-observer"

export default function DisordersSection() {
  const { ref, inView } = useInView({ triggerOnce: true, threshold: 0.1 })

  const disorders = [
    {
      icon: FaBrain,
      title: "Trastornos de Ansiedad",
      description: "Ansiedad generalizada, ataques de pánico, fobias específicas, trastorno obsesivo-compulsivo (TOC), estrés postraumático, ansiedad social."
    },
    {
      icon: FaCloudRain,
      title: "Trastornos del Estado de Ánimo",
      description: "Depresión mayor, distimia, trastorno bipolar, ciclotimia, trastornos adaptativos con estado de ánimo depresivo, depresión posparto."
    },
    {
      icon: FaUsers,
      title: "Problemas de Pareja y Familia",
      description: "Conflictos de comunicación, infidelidad, crisis de pareja, problemas en la crianza, divorcios, familias reconstituidas, mediación familiar."
    },
    {
      icon: FaMoon,
      title: "Trastornos del Sueño",
      description: "Insomnio, hipersomnia, pesadillas recurrentes, trastornos del ritmo circadiano, problemas de conciliación del sueño, apnea del sueño."
    },
    {
      icon: FaHeart,
      title: "Autoestima y Desarrollo Personal",
      description: "Inseguridad, baja autoestima, falta de habilidades sociales, asertividad, crecimiento personal, mindfulness, inteligencia emocional."
    },
    {
      icon: FaBriefcase,
      title: "Estrés Laboral",
      description: "Burnout, adaptación a cambios laborales, conflictos en el trabajo, gestión del estrés, desarrollo de carrera, equilibrio vida-trabajo."
    },
    {
      icon: FaHandHoldingHeart,
      title: "Trauma y Duelo",
      description: "Procesamiento de experiencias traumáticas, duelo por pérdidas significativas, EMDR, terapia de exposición, resiliencia, superación."
    },
    {
      icon: FaPuzzlePiece,
      title: "Trastornos de la Personalidad",
      description: "Trastorno límite, narcisista, evitativo, dependiente, obsesivo-compulsivo, histriónico y otras alteraciones de la personalidad."
    }
  ]

  return (
    <Box
      id="disorders"
      py={{ base: 16, md: 24 }}
      bg="white"
      position="relative"
      ref={ref}
    >
      {/* Decorative elements */}
      <Box position="absolute" bottom="10%" left="5%" w="200px" h="200px" borderRadius="50%" bg="rgba(255, 167, 38, 0.05)" />

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
              Trastornos que Tratamos
            </Heading>
            <Text fontSize={{ base: "lg", md: "xl" }} color="gray.600" maxW="800px">
              Especializados en diversas áreas de la salud mental
            </Text>
          </VStack>

          <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} gap={6} w="full">
            {disorders.map((disorder, index) => (
              <Box
                key={index}
                bg="white"
                p={6}
                borderRadius="xl"
                boxShadow="lg"
                opacity={inView ? 1 : 0}
                transform={inView ? "translateY(0)" : "translateY(30px)"}
                transition={`all 0.8s ${0.1 + index * 0.05}s`}
                _hover={{
                  transform: "translateY(-8px)",
                  boxShadow: "2xl"
                }}
              >
                <VStack gap={4} align="start">
                  <Box
                    bg="rgba(66, 133, 244, 0.1)"
                    p={3}
                    borderRadius="lg"
                    display="inline-flex"
                  >
                    <Icon as={disorder.icon} fontSize="2xl" color="#4285F4" />
                  </Box>
                  <Heading as="h3" fontSize="lg" color="gray.800">
                    {disorder.title}
                  </Heading>
                  <Text fontSize="sm" color="gray.700" lineHeight="1.7">
                    {disorder.description}
                  </Text>
                </VStack>
              </Box>
            ))}
          </SimpleGrid>
        </VStack>
      </Container>
    </Box>
  )
}
