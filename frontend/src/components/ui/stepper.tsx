import { Box, HStack, VStack, Text, Circle } from "@chakra-ui/react"
import { FiCheck } from "react-icons/fi"
import { useState } from "react"

export interface Step {
  title: string
  description?: string
}

export interface StepperProps {
  steps: Step[]
  activeStep: number
  colorScheme?: string
}

export interface UseStepsProps {
  index?: number
  count: number
}

export interface UseStepsReturn {
  activeStep: number
  goToNext: () => void
  goToPrevious: () => void
  setActiveStep: (index: number) => void
}

export function useSteps({ index = 0, count }: UseStepsProps): UseStepsReturn {
  const [activeStep, setActiveStep] = useState(index)

  const goToNext = () => {
    setActiveStep((prev) => Math.min(prev + 1, count - 1))
  }

  const goToPrevious = () => {
    setActiveStep((prev) => Math.max(prev - 1, 0))
  }

  return {
    activeStep,
    goToNext,
    goToPrevious,
    setActiveStep,
  }
}

export function Stepper({ steps, activeStep, colorScheme = "teal" }: StepperProps) {
  const colors = {
    teal: {
      active: "teal.500",
      complete: "teal.600",
      incomplete: "gray.300",
    },
    blue: {
      active: "blue.500",
      complete: "blue.600",
      incomplete: "gray.300",
    },
  }

  const colorSet = colors[colorScheme as keyof typeof colors] || colors.teal

  return (
    <HStack gap={0} w="full" align="start">
      {steps.map((step, index) => {
        const isComplete = index < activeStep
        const isActive = index === activeStep
        const isIncomplete = index > activeStep

        return (
          <HStack key={index} gap={0} flex={1} align="start">
            {/* Step Indicator */}
            <VStack gap={0} align="center" minW="fit-content">
              <Circle
                size="10"
                bg={
                  isComplete
                    ? colorSet.complete
                    : isActive
                      ? colorSet.active
                      : colorSet.incomplete
                }
                color="white"
                fontWeight="bold"
                fontSize="lg"
              >
                {isComplete ? <FiCheck /> : index + 1}
              </Circle>

              {/* Step Title and Description */}
              <VStack gap={0} mt={2} align="center">
                <Text
                  fontWeight={isActive ? "bold" : "medium"}
                  fontSize="sm"
                  color={isActive ? colorSet.active : "gray.600"}
                  textAlign="center"
                >
                  {step.title}
                </Text>
                {step.description && (
                  <Text fontSize="xs" color="gray.500" textAlign="center">
                    {step.description}
                  </Text>
                )}
              </VStack>
            </VStack>

            {/* Separator Line */}
            {index < steps.length - 1 && (
              <Box
                h="1px"
                flex={1}
                bg={isComplete ? colorSet.complete : colorSet.incomplete}
                mt="5"
                mx={2}
              />
            )}
          </HStack>
        )
      })}
    </HStack>
  )
}
